import os
import shutil
import struct
import logging
import traceback

from generated.formats.ms2 import Ms2File, Ms2Context
from generated.formats.ms2.compound.Ms2Root import Ms2Root

import generated.formats.ovl.versions as ovl_versions
from generated.formats.ovl_base.basic import ConvStream

from modules.formats.shared import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
from ovl_util import interaction
from ovl_util.interaction import showdialog


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
						self.detect_biosyn_format_from_user_input,):
					check = func()
					if check is not None:
						self.ovl.is_biosyn = check
						return check
		else:
			return False

	def detect_biosyn_format_from_user_input(self):
		logging.info("Detecting Biosyn format from user input")
		return showdialog(f"Does {self.ovl.name} use the mesh format from the Biosyn update?", ask=True)

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
		older_buffer_entry = 56
		biosyn_buffer_entry = 88
		buffer_frag = self._rel_at(self.root_ptr, 24)
		if buffer_frag:
			buffer_size = buffer_frag.struct_ptr.data_size
			if buffer_size:
				if not buffer_size % biosyn_buffer_entry:
					is_biosyn = True
				if not buffer_size % older_buffer_entry:
					is_older = True
		# print(f"is_biosyn {is_biosyn}")
		older_model_entry = 192
		biosyn_model_entry = 160
		model_infos_frag = self._rel_at(self.root_ptr, 32)
		if model_infos_frag:
			models_size = model_infos_frag.struct_ptr.data_size
			if models_size:
				if not models_size % biosyn_model_entry:
					is_biosyn = True
				if not models_size % older_model_entry:
					is_older = True
		if is_biosyn and not is_older:
			# good, trust it
			return True
		elif is_older and not is_biosyn:
			# good, trust it
			return False
		return None

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

	def get_buffer_presence(self):
		# some in JWE2 have a model2stream again
		expected_frag = b""
		if self.header.vertex_buffer_count:
			for stream in range(self.header.stream_count):
				expected_frag += struct.pack("<ii", 0, 0)
			for stream in range(self.header.vertex_buffer_count - self.header.stream_count):
				expected_frag += struct.pack("<ii", -1, 0)
		return expected_frag

	def collect(self):
		self.get_version()
		self.header = Ms2Root.from_stream(self.root_ptr.stream, self.context)
		self.header.read_ptrs(self.root_ptr.pool)
		# self.header.debug_ptrs()
		# print(self.header)
		expected_frag = self.get_buffer_presence()
		frag_data = self.header.buffers_presence.frag.struct_ptr.data
		if frag_data != expected_frag:
			logging.warning(
				f"Unexpected frag 2 ptr data ({frag_data}) for {self.file_entry.name}, expected ({expected_frag})")

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
		self.header.buffers_presence.data = ms2_file.buffers_presence
		for model_info in ms2_file.model_infos:
			model_info.materials.data = model_info.model.materials
			model_info.lods.data = model_info.model.lods
			model_info.objects.data = model_info.model.objects
			model_info.meshes.data = model_info.model.meshes
			for wrapper in model_info.model.meshes:
				# link the right buffer_info, then clear offset value
				wrapper.mesh.buffer_info.temp_index = wrapper.mesh.buffer_info.offset
				# undo what we did on export
				wrapper.mesh.buffer_info.offset = 0
		# print(self.header)
		# create root_entries and mesh data fragments
		for model_info, mdl2_name in zip(ms2_file.model_infos, ms2_file.mdl_2_names):
			mdl2_path = os.path.join(ms2_dir, mdl2_name+".mdl2")
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
				offset = wrapper.mesh.buffer_info.temp_index * self.header.buffer_infos.data[0].io_size
				self.attach_frag_to_ptr(wrapper.mesh.buffer_info, pool)
				self.ptr_relative(wrapper.mesh.buffer_info.frag.struct_ptr, self.header.buffer_infos.frag.struct_ptr, rel_offset=offset)

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
		# return self.dump_buffers(out_dir)
		name = self.root_entry.name
		logging.info(f"Writing {name}")
		# print(self.header)
		name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
		ms2_header = struct.pack("<II", self.context.biosyn, len(bone_infos))
		# write the ms2 file
		out_path = out_dir(name)
		out_paths = [out_path, ]
		with ConvStream() as stream:
			stream.write(ms2_header)
			self.header.write(stream)
			# present since DLA
			if self.header.buffers_presence.data is not None:
				self.header.buffers_presence.data.write(stream)
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
				ptrs = set(wrapper.mesh.buffer_info.frag.struct_ptr for model_info in self.header.model_infos.data for wrapper in model_info.meshes.data)
				# get the sorted binary representations
				buffer_infos = [ptr.data for ptr in sorted(ptrs, key=lambda ptr: ptr.data_offset)]
				# turn the offset value of the pointers into a valid index
				for model_info in self.header.model_infos.data:
					for wrapper in model_info.meshes.data:
						buffer_info_bytes = wrapper.mesh.buffer_info.frag.struct_ptr.data
						wrapper.mesh.buffer_info.offset = buffer_infos.index(buffer_info_bytes)
				if self.header.buffer_infos.data is not None:
					self.header.buffer_infos.data.write(stream)
				self.header.model_infos.data.write(stream)
				for model_info in self.header.model_infos.data:
					for ptr in (model_info.materials, model_info.lods, model_info.objects, model_info.meshes):
						ptr.data.write(stream)
		
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
			self.ovl.create_file(ms2_path)
		except BaseException as err:
			traceback.print_exc()
			logging.warning(err)
		# delete temp dir again
		shutil.rmtree(temp_dir)
