import io
import os
import struct
import logging

from generated.formats.ms2 import Ms2File, Ms2Context
from generated.formats.ms2.structs.Buffer0 import Buffer0
from generated.formats.ms2.structs.ModelstreamHeader import ModelstreamHeader
from generated.formats.ms2.structs.Ms2Root import Ms2Root

import generated.formats.ovl.versions as ovl_versions

from generated.formats.base.structs.PadAlign import get_padding
from modules.formats.BaseFormat import BaseFile, MemStructLoader, MimeVersionedLoader
from modules.helpers import as_bytes


class Mdl2Loader(BaseFile):
	extension = ".mdl2"
	can_extract = False

	def create(self, file_path):
		self.root_ptr = (None, 0)


class Model2streamLoader(MimeVersionedLoader):
	extension = ".model2stream"
	target_class = ModelstreamHeader
	can_extract = False

	def create(self, file_path):
		self.header = self.target_class(self.context)
		# JWE2, PC2
		if self.context.version >= 52:
			self.header.lod_index = int(self.basename[-1])
		self.write_memory_data()
	
	def create_data(self, buffer_data):
		self.create_data_entry((buffer_data,))
		for buffer in self.data_entry.buffers:
			buffer.index = 2
		self.data_entry.size_1 = 0
		self.data_entry.size_2 = len(buffer_data)


class Ms2Loader(MemStructLoader):
	extension = ".ms2"
	target_class = Ms2Root

	def link_streams(self):
		"""Collect other loaders"""
		# if the ms2 name ends in a trailing underscore, remove it
		bare_name = self.basename.rstrip("_")
		self._link_streams(f"{bare_name}{lod_i}.model2stream" for lod_i in range(4))

	def get_version(self):
		pool, offset = self.root_ptr
		data = pool.get_data_at(offset)
		version = struct.unpack(f"I", data[:4])[0]
		self.context = Ms2Context()
		self.context.version = version
		self.context.biosyn = int(not self.ovl.is_dev)

	def collect(self):
		self.get_version()
		pool, offset = self.root_ptr
		stream = pool.stream_at(offset)
		self.header = Ms2Root.from_stream(stream, self.context)
		try:
			self.header.read_ptrs(pool, debug=self.ovl.do_debug)
			if self.header.buffer_pointers.data:
				for i, buffer_presence in enumerate(self.header.buffer_pointers.data):
					d = buffer_presence.dependency_name
					if d.pool_index != -1 and not d.data:
						logging.warning(f"Streamed mesh buffer {i} for {self.name} has no dependency to a .model2stream file")
		except:
			logging.exception(f"MS2 collecting failed")

	def get_first_model_offset(self):
		for model_info in self.header.model_infos.data:
			for ptr in (model_info.materials, model_info.lods, model_info.objects, model_info.meshes):
				if ptr.target_offset is not None:
					return ptr.target_pool, ptr.target_offset
		return self.header.model_infos.target_pool, None

	def create(self, file_path):
		ms2_dir = os.path.dirname(file_path)
		if os.path.basename(ms2_dir) == "backups":
			raise UserWarning(f"Ignored backup '{file_path}'")
		ms2_file = Ms2File()
		ms2_file.load(file_path, read_bytes=True)
		# print(ms2_file)
		# print(ms2_file.models_reader.bone_infos)
		# for m in ms2_file.model_infos:
		# 	print(m.model)
			# print(m.bone_info)
		self.ovl.is_dev = int(not ms2_file.biosyn)
		self.context = Ms2Context()
		self.context.version = ms2_file.info.version
		self.context.biosyn = ms2_file.biosyn

		self.header = ms2_file.info
		# fix up the pointers
		self.header.buffer_infos.data = ms2_file.buffer_infos
		self.header.model_infos.data = ms2_file.model_infos
		self.header.buffer_pointers.data = ms2_file.buffer_pointers
		buffer_infos = self.header.buffer_infos
		for model_info in ms2_file.model_infos:
			model_info.materials.data = model_info.model.materials
			model_info.lods.data = model_info.model.lods
			model_info.objects.data = model_info.model.objects
			model_info.meshes.data = model_info.model.meshes
			for wrapper in model_info.model.meshes:
				wrapper.mesh.stream_info.update_target(buffer_infos)
		# print(self.header)
		# determine ovs names. these differ by game version and there is no real way to predict them
		# older JWE2 versions used "HighPolyModels" exclusively
		# current JWE2 as of 2022-09-17, even when there is just 1 stream (as in DEC_RaptorPaddock.ovl models2lods.ms2)
		if len(ms2_file.modelstream_names) == 1:
			# same idiosyncrasy as in texturestreams
			indices = [1, ]
		else:
			indices = range(len(ms2_file.modelstream_names))
		ovs_lut = {n: f"Models_L{i}" for n, i in zip(ms2_file.modelstream_names, indices)}
		# create modelstreams for buffers that have them
		for buffer_info, buffer_presence in zip(self.header.buffer_infos.data, self.header.buffer_pointers.data):
			if buffer_info.name == "STATIC":
				buffer_presence.dependency_name.pool_index = -1
			else:
				buffer_presence.dependency_name.pool_index = 0
				buffer_presence.dependency_name.data = buffer_info.name
				modelstream_name = f"{buffer_info.name}.model2stream"
				modelstream_loader = self.ovl.create_file(f"dummy/{modelstream_name}", modelstream_name, ovs_name=ovs_lut[buffer_info.name])
				modelstream_loader.create_data(ms2_file.get_all_bytes(buffer_info))
				self.streams.append(modelstream_loader)

		# create root_entries and mesh data fragments
		for model_info, mdl2_barename in zip(ms2_file.model_infos, ms2_file.mdl_2_names):
			mdl2_name = f"{mdl2_barename}.mdl2"
			mdl2_path = os.path.join(ms2_dir, mdl2_name)
			mdl2_loader = self.ovl.create_file(mdl2_path, mdl2_name)
			self.children.append(mdl2_loader)

		# create ms2 data
		self.create_data_entry(tuple(ms2_file.buffers))
		# standard layout
		# size_1 = sum of 0 + 1
		# size_2 = 2

		# write the final memstruct
		self.write_memory_data()
		# link some more pointers
		pool = self.header.model_infos.target_pool
		first_model_pool, first_model_offset = self.get_first_model_offset()
		for model_info in self.header.model_infos.data:
			# link first_model pointer
			self.attach_frag_to_ptr(pool, model_info.first_model.io_start, first_model_pool, first_model_offset)

	def update(self):
		if ovl_versions.is_pz16(self.ovl):
			logging.debug(f"Updating MS2 name_buffer with padding for {self.name}")
			name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
			# fix ms2s that have additional 'padding'
			# first remove trailing zeroes, add zstr terminator back in
			name_buffer_truncated = name_buffer.rstrip(b"\x00") + b"\x00"
			# make sure name_buffer is padded to 4 bytes
			padding = get_padding(len(name_buffer_truncated), 4)
			self.data_entry.update_data([name_buffer_truncated + padding, bone_infos, verts])
	
	def extract(self, out_dir):
		self.get_version()
		logging.info(f"Writing {self.name}")
		# print(self.header)
		name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
		# print(name_buffer, bone_infos, verts)
		ms2_header = struct.pack("<III", self.context.biosyn, len(bone_infos), len(self.streams))
		# write the ms2 file
		out_path = out_dir(self.name)
		out_paths = [out_path, ]
		context = self.header.context
		with open(out_path, 'wb') as stream:
			stream.write(ms2_header)
			self.header.to_stream(self.header, stream, context)
			# present since DLA
			if self.header.buffer_pointers.data is not None:
				self.header.buffer_pointers.data.to_stream(self.header.buffer_pointers.data, stream, context)
			for mdl2_loader in self.children:
				# logging.debug(f"Writing {mdl2_loader.name}")
				stream.write(as_bytes(mdl2_loader.basename))
			for loader in self.streams:
				stream.write(as_bytes(loader.basename))
			stream.write(name_buffer)
			# export each mdl2
			if self.header.version > 39:
				# this corresponds to pc buffer 1 already
				# store buffer index in Pointer.pool_index
				for model_info in self.header.model_infos.data:
					for wrapper in model_info.meshes.data:
						wrapper.mesh.stream_info.update_index(self.header.buffer_infos.data)
				if self.header.buffer_infos.data is not None:
					self.header.buffer_infos.data.to_stream(self.header.buffer_infos.data, stream, context)
				self.header.model_infos.data.to_stream(self.header.model_infos.data, stream, context)
				for model_info in self.header.model_infos.data:
					for ptr in (model_info.materials, model_info.lods, model_info.objects, model_info.meshes):
						ptr.data.to_stream(ptr.data, stream, context)
			stream.write(bone_infos)
			# logging.debug(f"Writing verts at {stream.tell()}")
			stream.write(verts)
			for loader in self.streams:
				# logging.debug(f"Writing {loader.name} at {stream.tell()}")
				logging.debug(f"Stream {loader.name} is in {loader.ovs.arg.name}")
				stream.write(loader.data_entry.buffer_datas[0])
				
		return out_paths
	
	def get_ms2_buffer_datas(self):
		assert self.data_entry
		all_buffer_bytes = self.data_entry.buffer_datas
		name_buffer = all_buffer_bytes[0]
		bone_infos = all_buffer_bytes[1]
		verts = b"".join(all_buffer_bytes[2:])
		return name_buffer, bone_infos, verts

	def validate(self):
		"""Verify that the used materials exist in the OVL"""
		missing_materials = set()
		buffer_0_stream = io.BytesIO(self.data_entry.buffer_datas[0])
		names_buffer = Buffer0.from_stream(buffer_0_stream, self.context, self.header)
		if self.header.version > 39:
			for model_info in self.header.model_infos.data:
				for material in model_info.materials.data:
					material_name = names_buffer.names[material.name_index].lower()
					fgm_name = f"{material_name}.fgm"
					if ovl_versions.is_jwe(self.ovl) or ovl_versions.is_jwe2(self.ovl) and fgm_name == "airliftstraps.fgm":
						# don't cry about this
						continue
					# if fgm_name not in self.ovl.loaders:
					# 	missing_materials.add(fgm_name)
		if missing_materials:
			mats = '\n'.join(missing_materials)
			msg = f"The following materials are used by {self.name}, but are missing from the OVL:\n" \
				f"{mats}\n" \
				f"This will crash unless you are linking the materials from another OVL."
			raise UserWarning(msg)

	def rename_content(self, name_tuples):
		logging.info("Renaming inside .ms2")
		with self.get_tmp_dir_func() as out_dir_func:
			try:
				ms2_path = self.extract(out_dir_func)[0]
				# open the ms2 file
				ms2_file = Ms2File()
				ms2_file.load(ms2_path, read_bytes=True)
				# rename the materials
				ms2_file.rename(name_tuples)
				# update the hashes & save
				ms2_file.save(ms2_path)
				# inject again
				loader = self.ovl.create_file(ms2_path, self.name)
				self.ovl.register_loader(loader)
			except:
				logging.exception(f"Renaming inside {self.name} failed")
