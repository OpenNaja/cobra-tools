import os
import shutil
import struct
import logging
import traceback

from generated.formats.ms2 import Ms2File, Ms2Context
from generated.formats.ms2.compounds.Ms2Root import Ms2Root

import generated.formats.ovl.versions as ovl_versions
from io import BytesIO

from generated.formats.base.compounds.PadAlign import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
from ovl_util import interaction


class Mdl2Loader(BaseFile):
	extension = ".mdl2"

	def create(self):
		self.create_root_entry()
		self.root_entry.struct_ptr.pool_index = -1


class Model2streamLoader(BaseFile):
	extension = ".model2stream"

	def extract(self, out_dir):
		stream_path = out_dir(self.file_entry.name)
		with open(stream_path, 'wb') as outfile:
			outfile.write(self.data_entry.buffer_datas[0])
		return stream_path,

	def create(self):
		self.create_root_entry()

		if ovl_versions.is_jwe2(self.ovl):
			lod_index = int(self.file_entry.basename[-1])
			root_data = struct.pack("<QQ", 0, lod_index)
		else:
			# JWE1, PZ, PC  all untested 
			root_data = struct.pack("<Q", 0)  
		self.write_data_to_pool(self.root_entry.struct_ptr, self.file_entry.pool_type, root_data)
		self.create_data_entry((self.get_content(self.file_entry.path),))
		for buffer in self.data_entry.buffers:
			buffer.index = 2
		temp1 = self.data_entry.size_1
		temp2 = self.data_entry.size_2
		self.data_entry.size_1 = temp2
		self.data_entry.size_2 = temp1


class Ms2Loader(BaseFile):
	extension = ".ms2"

	@staticmethod
	def _rel_at(parent_ptr, offset):
		for frag in parent_ptr.children:
			if frag.link_ptr.data_offset == parent_ptr.data_offset + offset:
				return frag

	def detect_biosyn_format(self):
		logging.info("Detecting Biosyn format")
		if ovl_versions.is_jwe2(self.ovl):
			if self.ovl.is_biosyn is not None:
				return self.ovl.is_biosyn
			else:
				for func in (
						self.detect_biosyn_format_from_manis,
						self.detect_biosyn_format_from_ptrs,
						self.detect_biosyn_default,):
					check = func()
					if check is not None:
						self.ovl.is_biosyn = check
						return check
		else:
			return False

	def detect_biosyn_default(self):
		logging.info("Assuming Biosyn format")
		# todo - query a biosyn_default setting on ovl, set before from gui or config
		return True

	def detect_biosyn_format_from_manis(self):
		logging.info("Detecting Biosyn format from .manis")
		for mime in self.ovl.mimes:
			if mime.ext == ".manis":
				# JWE2 pre Biosyn
				if mime.mime_version == 261:
					return False
				# JWE2 post Biosyn
				elif mime.mime_version == 262:
					return True
		return None

	def detect_biosyn_format_from_ptrs(self):
		logging.info("Detecting Biosyn format from pointers")
		is_biosyn = False
		is_older = False
		# BufferInfo
		is_biosyn, is_older = self._biosyn_check_ptr(is_biosyn, is_older, 24, 56, 88)
		# ModelInfo
		is_biosyn, is_older = self._biosyn_check_ptr(is_biosyn, is_older, 32, 192, 160)
		# good, trust it
		if is_biosyn and not is_older:
			return True
		elif is_older and not is_biosyn:
			return False
		# inconclusive result, don't trust it
		return None

	def _biosyn_check_ptr(self, is_biosyn, is_older, offset, older_size, biosyn_size):
		frag = self._rel_at(self.root_ptr, offset)
		if frag:
			size = frag.struct_ptr.data_size
			if size:
				if not size % biosyn_size:
					is_biosyn = True
				if not size % older_size:
					is_older = True
		return is_biosyn, is_older

	def link_streams(self):
		"""Collect other loaders"""
		# if the ms2 name ends in a trailing underscore, remove it
		bare_name = self.file_entry.basename.rstrip("_")
		self._link_streams(f"{bare_name}{lod_i}.model2stream" for lod_i in range(4))

	def get_version(self):
		version = struct.unpack(f"I", self.root_ptr.data[:4])[0]
		self.context = Ms2Context()
		self.context.version = version
		self.context.biosyn = self.detect_biosyn_format()
		logging.info(f"context.biosyn {self.context.biosyn}")

	def collect(self):
		self.get_version()
		self.header = Ms2Root.from_stream(self.root_ptr.stream, self.context)
		self.header.read_ptrs(self.root_ptr.pool)
		for i, buffer_presence in enumerate(self.header.buffer_pointers.data):
			d = buffer_presence.dependency_name
			if d.offset != -1 and not d.data:
				logging.warning(f"Streamed mesh buffer {i} for {self.file_entry.name} has no dependency to a .model2stream file")
		# print(self.header)

	def get_first_model_frag(self):
		for model_info in self.header.model_infos.data:
			for ptr in (model_info.materials, model_info.lods, model_info.objects, model_info.meshes):
				if ptr.frag:
					return ptr.frag

	def create(self):
		ms2_file = Ms2File()
		ms2_file.load(self.file_entry.path, read_bytes=True)
		ms2_dir = os.path.dirname(self.file_entry.path)

		self.create_root_entry()
		self.header = ms2_file.info
		# fix up the pointers
		self.header.buffer_infos.data = ms2_file.buffer_infos
		self.header.model_infos.data = ms2_file.model_infos
		self.header.buffer_pointers.data = ms2_file.buffer_pointers
		for model_info in ms2_file.model_infos:
			model_info.materials.data = model_info.model.materials
			model_info.lods.data = model_info.model.lods
			model_info.objects.data = model_info.model.objects
			model_info.meshes.data = model_info.model.meshes
			for wrapper in model_info.model.meshes:
				# link the right buffer_info, then clear offset value
				wrapper.mesh.stream_info.temp_index = wrapper.mesh.stream_info.offset
				# undo what we did on export
				wrapper.mesh.stream_info.offset = 0
		# print(self.header)
		# determine ovs names. these differ by game version and there is no real way to predict them
		# older JWE2 versions used "HighPolyModels" exclusively
		# current JWE2 as of 2022-09-17, even when there is just 1 stream (as in DEC_RaptorPaddock.ovl models2lods.ms2)
		if len(ms2_file.modelstream_names) == 1:
			# same idiosyncrasy as in texturestreams
			indices = [1, ]
		else:
			indices = range(len(ms2_file.modelstream_names))
		ovs_names = [f"Models_L{i}" for i in indices]
		# create modelstreams
		for modelstream_name, ovs_name in zip(ms2_file.modelstream_names, ovs_names):
			modelstream_path = os.path.join(ms2_dir, modelstream_name)
			modelstream_loader = self.ovl.create_file(modelstream_path, ovs_name=ovs_name)
			self.streams.append(modelstream_loader)
			# todo - store stream name in self.header.buffer_pointers so that a dependency is created

		# create root_entries and mesh data fragments
		for model_info, mdl2_name in zip(ms2_file.model_infos, ms2_file.mdl_2_names):
			mdl2_path = os.path.join(ms2_dir, f"{mdl2_name}.mdl2")
			mdl2_loader = self.ovl.create_file(mdl2_path)
			self.children.append(mdl2_loader)

		# create ms2 data
		self.create_data_entry(ms2_file.buffers)
		# write the final memstruct
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)
		# link some more pointers
		pool = self.header.model_infos.frag.struct_ptr.pool
		first_model_frag = self.get_first_model_frag()
		for model_info in self.header.model_infos.data:
			# link first_model pointer
			if not first_model_frag:
				logging.error(f"MS2 {self.file_entry.name} has no pointers on any model")
			self.attach_frag_to_ptr(model_info.first_model, pool)
			self.ptr_relative(model_info.first_model.frag.struct_ptr, first_model_frag.struct_ptr)
			for wrapper in model_info.model.meshes:
				# buffer_infos have been written, now make this mesh's buffer_info pointer point to the right entry
				offset = wrapper.mesh.stream_info.temp_index * self.header.buffer_infos.data[0].io_size
				self.attach_frag_to_ptr(wrapper.mesh.stream_info, pool)
				self.ptr_relative(wrapper.mesh.stream_info.frag.struct_ptr, self.header.buffer_infos.frag.struct_ptr, rel_offset=offset)
		# for f in self.fragments:
		# 	print(f, f.link_ptr.data_size, f.struct_ptr.data_size)

	def update(self):
		if ovl_versions.is_pz16(self.ovl):
			logging.info(f"Updating MS2 name_buffer with padding for {self.root_entry.name}")
			name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
			# fix ms2s that have additional 'padding'
			# first remove trailing zeroes, add zstr terminator back in
			name_buffer_truncated = name_buffer.rstrip(b"\x00") + b"\x00"
			# make sure name_buffer is padded to 4 bytes
			padding = get_padding(len(name_buffer_truncated), 4)
			self.data_entry.update_data([name_buffer_truncated + padding, bone_infos, verts])
	
	def extract(self, out_dir):
		self.get_version()
		name = self.root_entry.name
		logging.info(f"Writing {name}")
		# print(self.header)
		name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
		ms2_header = struct.pack("<III", self.context.biosyn, len(bone_infos), len(self.streams))
		# write the ms2 file
		out_path = out_dir(name)
		out_paths = [out_path, ]
		context = self.header.context
		with BytesIO() as stream:
			stream.write(ms2_header)
			self.header.to_stream(self.header, stream, context)
			# present since DLA
			if self.header.buffer_pointers.data is not None:
				self.header.buffer_pointers.data.to_stream(self.header.buffer_pointers.data, stream, context)
			for mdl2_loader in self.children:
				mdl2_entry = mdl2_loader.file_entry
				logging.debug(f"Writing {mdl2_entry.name}")
				stream.write(as_bytes(mdl2_entry.basename))
			for loader in self.streams:
				stream.write(as_bytes(loader.file_entry.name))
				out_paths.extend(loader.extract(out_dir))
			stream.write(name_buffer)
			# export each mdl2
			if self.header.version > 39:
				# this corresponds to pc buffer 1 already
				# handle multiple buffer infos
				# grab all unique ptrs to buffer infos
				ptrs = set(wrapper.mesh.stream_info.frag.struct_ptr for model_info in self.header.model_infos.data for wrapper in model_info.meshes.data)
				# get the sorted binary representations
				buffer_infos = [ptr.data for ptr in sorted(ptrs, key=lambda ptr: ptr.data_offset)]
				# turn the offset value of the pointers into a valid index
				for model_info in self.header.model_infos.data:
					for wrapper in model_info.meshes.data:
						buffer_info_bytes = wrapper.mesh.stream_info.frag.struct_ptr.data
						wrapper.mesh.stream_info.offset = buffer_infos.index(buffer_info_bytes)
				if self.header.buffer_infos.data is not None:
					self.header.buffer_infos.data.to_stream(self.header.buffer_infos.data, stream, context)
				self.header.model_infos.data.to_stream(self.header.model_infos.data, stream, context)
				for model_info in self.header.model_infos.data:
					for ptr in (model_info.materials, model_info.lods, model_info.objects, model_info.meshes):
						ptr.data.to_stream(ptr.data, stream, context)
		
			with open(out_path, 'wb') as outfile:
				outfile.write(stream.getvalue())
				outfile.write(bone_infos)
				outfile.write(verts)
		# m = Ms2File()
		# m.load(out_path, read_editable=True)
		# m.load(out_path, read_editable=False)
		# m.save(out_path+"_.ms2")
		# print(m)
		return out_paths
	
	def get_ms2_buffer_datas(self):
		assert self.data_entry
		all_buffer_bytes = self.data_entry.buffer_datas
		name_buffer = all_buffer_bytes[0]
		bone_infos = all_buffer_bytes[1]
		verts = b"".join(all_buffer_bytes[2:])
		return name_buffer, bone_infos, verts

	def check_materials(self, ms2_file):
		"""Verify that the used materials exist in the OVL"""
		missing_materials = set()
		for model_info, mdl2_name in zip(ms2_file.model_infos, ms2_file.mdl_2_names):
			for material in model_info.model.materials:
				fgm_name = f"{material.name.lower()}.fgm"
				if ovl_versions.is_jwe(self.ovl) or ovl_versions.is_jwe2(self.ovl) and fgm_name == "airliftstraps.fgm":
					# don't cry about this
					continue
				if fgm_name not in self.ovl.loaders:
					missing_materials.add(fgm_name)
		if missing_materials:
			mats = '\n'.join(missing_materials)
			msg = f"The following materials are used by {self.file_entry.name}, but are missing from the OVL:\n" \
				f"{mats}\n" \
				f"This will crash unless you are importing the materials from another OVL. Inject anyway?"
			if not interaction.showdialog(msg, ask=True):
				raise UserWarning("Injection was canceled by the user")

	def rename_content(self, name_tuples):
		logging.info("Renaming inside .ms2")
		temp_dir, out_dir_func = self.get_tmp_dir()
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
			self.remove()
			loader = self.ovl.create_file(ms2_path)
			self.ovl.register_loader(loader)
		except BaseException as err:
			traceback.print_exc()
			logging.warning(err)
		# delete temp dir again
		shutil.rmtree(temp_dir)
