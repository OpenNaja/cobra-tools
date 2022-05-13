import os
import shutil
import struct
import logging

from generated.formats.ms2 import Ms2File, Ms2Context
from generated.formats.ms2.compound.Ms2Root import Ms2Root

import generated.formats.ovl.versions as ovl_versions
from generated.formats.ovl_base.basic import ConvStream

from modules.formats.shared import get_versions, get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
from ovl_util import interaction


class Mdl2Loader(BaseFile):
	extension = ".mdl2"

	def collect(self):
		self.assign_root_entry()


class Model2streamLoader(BaseFile):
	extension = ".model2stream"

	def extract(self, out_dir, show_temp_files, progress_callback):
		stream_path = out_dir(self.file_entry.name)
		with open(stream_path, 'wb') as outfile:
			outfile.write(self.root_entry.data_entry.buffer_datas[0])
		return stream_path,


class Ms2Loader(BaseFile):
	extension = ".ms2"

	def link_streams(self):
		"""Collect other loaders"""
		# if the ms2 name ends in a trailing underscore, remove it
		bare_name = self.file_entry.basename.rstrip("_")
		self._link_streams(f"{bare_name}{lod_i}.model2stream" for lod_i in range(4))

	def get_version(self):
		version = struct.unpack(f"I", self.root_ptr.data[:4])[0]
		vdic = {"version": version}
		self.context = Ms2Context()
		self.context.version = version
		return vdic

	def get_frag_3(self, header):
		# some in JWE2 have a model2stream again
		expected_frag = b""
		if self.header.vertex_buffer_count:
			for stream in range(self.header.stream_count):
				expected_frag += struct.pack("<ii", 0, 0)
			for stream in range(self.header.vertex_buffer_count - self.header.stream_count):
				expected_frag += struct.pack("<ii", -1, 0)
		return expected_frag

	def collect(self):
		self.assign_root_entry()
		self.get_version()
		self.header = Ms2Root.from_stream(self.root_ptr.stream, self.context)
		self.header.read_ptrs(self.root_ptr.pool)
		# self.header.debug_ptrs()
		# print(self.header)
		# old JWE1 still uses 1 fragment
		if self.header.version > 39:
			if self.root_ptr.data_size != 48:
				logging.warning(f"Unexpected Root size ({self.root_ptr.data_size}) for {self.file_entry.name}")
			expected_frag = self.get_frag_3(self.header)
			frag_data = self.header.buffers_presence.frag.struct_ptr.data
			if frag_data != expected_frag:
				logging.warning(
					f"Unexpected frag 2 ptr data ({frag_data}) for {self.file_entry.name}, expected ({expected_frag})")

	def create(self):
		ms2_file = Ms2File()
		ms2_file.load(self.file_entry.path, read_bytes=True)
		ms2_dir = os.path.dirname(self.file_entry.path)

		self.root_entry = self.create_root_entry(self.file_entry)

		self.header = ms2_file.info
		# fix up the pointers
		self.header.buffer_infos.data = ms2_file.buffer_infos
		self.header.model_infos.data = ms2_file.model_infos
		# todo - maybe store in ms2 file
		self.header.buffers_presence.data = self.get_frag_3(self.header)
		for model_info in ms2_file.model_infos:
			model_info.materials.data = model_info.model.materials
			model_info.lods.data = model_info.model.lods
			model_info.objects.data = model_info.model.objects
			model_info.meshes.data = model_info.model.meshes
			# just set empty data here, link later
			model_info.first_materials.data = b""
			for mesh in model_info.model.meshes:
				mesh.buffer_info.data = b""
				# link the right buffer_info, then clear offset value
				mesh.buffer_info.temp_index = mesh.buffer_info.offset
				# undo what we did on export
				mesh.buffer_info.offset = 0
		# print(self.header)
		# create root_entries and mesh data fragments
		for model_info, mdl2_name in zip(ms2_file.model_infos, ms2_file.mdl_2_names):
			mdl2_path = os.path.join(ms2_dir, mdl2_name+".mdl2")
			mdl2_file_entry = self.get_file_entry(mdl2_path)

			mdl2_entry = self.create_root_entry(mdl2_file_entry)
			mdl2_entry.struct_ptr.pool_index = -1
			self.root_entry.children.append(mdl2_entry)

		# create ms2 data
		self.create_data_entry(self.root_entry, ms2_file.buffers)
		# write the final memstruct
		self.header.write_ptrs(self, self.ovs, self.root_ptr, self.file_entry.pool_type)
		# link some more pointers
		pool = self.header.model_infos.frag.struct_ptr.pool
		for model_info in self.header.model_infos.data:
			# link first_materials pointer
			first_materials = self.header.model_infos.data[0].materials.frag
			assert first_materials
			model_info.first_materials.frag = self.create_fragment(self.root_entry)
			model_info.first_materials.frag.link_ptr.data_offset = model_info.first_materials.io_start
			model_info.first_materials.frag.link_ptr.pool = pool
			self.ptr_relative(model_info.first_materials.frag.struct_ptr, first_materials.struct_ptr)
			for mesh in model_info.model.meshes:
				# buffer_infos have been written, now make this mesh's buffer_info pointer point to the right entry
				offset = mesh.buffer_info.temp_index * self.header.buffer_infos.data[0].io_size
				mesh.buffer_info.frag = self.create_fragment(self.root_entry)
				mesh.buffer_info.frag.link_ptr.data_offset = mesh.buffer_info.io_start
				mesh.buffer_info.frag.link_ptr.pool = pool
				self.ptr_relative(mesh.buffer_info.frag.struct_ptr, self.header.buffer_infos.frag.struct_ptr, rel_offset=offset)

	def update(self):
		if ovl_versions.is_pz16(self.ovl):
			logging.info(f"Updating MS2 buffer 0 with padding for {self.root_entry.name}")
			name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
			# make sure buffer 0 is padded to 4 bytes
			padding = get_padding(len(name_buffer), 4)
			if padding:
				self.root_entry.data_entry.update_data([name_buffer + padding, bone_infos, verts])
	
	def extract(self, out_dir, show_temp_files, progress_callback):
		self.get_version()
		name = self.root_entry.name
		logging.info(f"Writing {name}")
		name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
		# truncate to 48 bytes for PZ af_keeperbodyparts
		ms2_general_info_data = self.root_entry.struct_ptr.data[:48]
		ms2_header = struct.pack("<I", len(bone_infos))

		# write the ms2 file
		out_path = out_dir(name)
		out_paths = [out_path, ]
		with ConvStream() as stream:
			stream.write(ms2_header)
			stream.write(ms2_general_info_data)
			for mdl2_entry in self.root_entry.children:
				logging.debug(f"Writing {mdl2_entry.name}")
				stream.write(as_bytes(mdl2_entry.basename))
			for loader in self.streams:
				stream.write(as_bytes(loader.file_entry.basename))
				out_paths.extend(loader.extract(out_dir, show_temp_files, progress_callback))
			stream.write(name_buffer)
			# export each mdl2
			if self.header.version > 39:
				# this corresponds to pc buffer 1 already
				# handle multiple buffer infos
				# grab all unique ptrs to buffer infos
				ptrs = set(mesh.buffer_info.frag.struct_ptr for model_info in self.header.model_infos.data for mesh in model_info.meshes.data)
				# get the sorted binary representations
				buffer_infos = [ptr.data for ptr in sorted(ptrs, key=lambda ptr: ptr.data_offset)]
				# turn the offset value of the pointers into a valid index
				for model_info in self.header.model_infos.data:
					for mesh in model_info.meshes.data:
						buffer_info_bytes = mesh.buffer_info.frag.struct_ptr.data
						mesh.buffer_info.offset = buffer_infos.index(buffer_info_bytes)
				stream.write(b"".join(buffer_infos))
				self.header.model_infos.data.write(stream)
				for model_info in self.header.model_infos.data:
					for ptr in (model_info.materials, model_info.lods, model_info.objects, model_info.meshes):
						ptr.data.write(stream)
		
			with open(out_path, 'wb') as outfile:
				outfile.write(stream.getvalue())
				outfile.write(bone_infos)
				outfile.write(verts)
		# m = Ms2File()
		# m.load(out_path)
		# m.load(out_path, read_editable=True)
		# m.save(out_path+"_.ms2")
		# print(m)
		return out_paths
	
	def get_ms2_buffer_datas(self):
		assert self.root_entry.data_entry
		all_buffer_bytes = self.root_entry.data_entry.buffer_datas
		name_buffer = all_buffer_bytes[0]
		bone_infos = all_buffer_bytes[1]
		verts = b"".join(all_buffer_bytes[2:])
		return name_buffer, bone_infos, verts
	
	def load(self, ms2_file_path):
		logging.info(f"Injecting MS2")
		self.remove(remove_file=False)
		self.file_entry.path = ms2_file_path
		self.create()

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
		temp_dir, out_dir_func = self.get_tmp_dir()
		try:
			ms2_path = self.extract(out_dir_func, False, None)[0]
			# open the ms2 file
			ms2_file = Ms2File()
			ms2_file.load(ms2_path, read_bytes=True)
			# rename the materials
			ms2_file.rename(name_tuples)
			# update the hashes & save
			ms2_file.save(ms2_path)
			# inject again
			self.load(ms2_path)
		except BaseException as err:
			logging.warning(err)
		# delete temp dir again
		shutil.rmtree(temp_dir)
