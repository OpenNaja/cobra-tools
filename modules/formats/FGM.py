import logging
import struct

from generated.formats.fgm.compound.FgmHeader import FgmHeader
from generated.formats.ovl_base.basic import ConvStream
from modules.formats.BaseFormat import MemStructLoader
from modules.formats.shared import get_versions, get_padding
from modules.helpers import as_bytes, zstr
from generated.formats.fgm import FgmFile


class FgmLoader(MemStructLoader):
	target_class = FgmHeader
	extension = ".fgm"

	def create(self):
		fgm_data = self._get_data(self.file_entry.path)
		# first create dependencies
		for tex_name in fgm_data.texture_files:
			self.create_dependency(f"{tex_name}.tex")
		self.header = fgm_data.fgm_info
		# link the pointers
		self.header.textures.data = fgm_data.textures
		self.header.attributes.data = fgm_data.attributes
		self.header.data_lib.data = fgm_data.data_bytes
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.struct_ptr
		self.header.write_ptrs(self, self.ovs, ss_ptr, self.file_entry.pool_type)
		self.create_data_entry(self.sized_str_entry, (fgm_data.buffer_bytes,))

		if fgm_data.texture_files:
			for dependency in self.file_entry.dependencies:
				self.write_to_pool(dependency.link_ptr, 2, b"\x00" * 8)
			# points to the start of the dependencies region
			self.header.dependencies.frag = self.create_fragments(self.sized_str_entry, 1)[0]
			rel_off = self.header.dependencies.io_start - self.header.io_start
			self.ptr_relative(self.header.dependencies.frag.link_ptr, ss_ptr, rel_offset=rel_off)
			self.ptr_relative(self.header.dependencies.frag.struct_ptr, self.file_entry.dependencies[0].link_ptr)

	def collect(self):
		super().collect()
		self.header.debug_ptrs()
		# print(self.header)

	def load(self, file_path):
		# todo - replace self.header, and update the pointer datas
		# self.header = fgm_data
		fgm_data = self._get_data(file_path)
		datas, sizedstr_bytes = self._get_frag_datas(fgm_data)

		self.sized_str_entry.data_entry.update_data((fgm_data.buffer_bytes,))
		self.sized_str_entry.struct_ptr.update_data(as_bytes(self.header))

		# inject fragment datas
		for ptr, data in zip(self._ptrs(), datas):
			# print(pointer, pointer.data, pointer.frag)
			frag = ptr.frag
			if not frag:
				continue
			logging.debug(f"frag: len old {len(frag.struct_ptr.data)} len padding {len(frag.struct_ptr.padding)} len new {len(data)}")
			frag.struct_ptr.update_data(data, update_copies=True)

		# update dependencies on ovl
		for dependency, tex_name in zip(self.file_entry.dependencies, fgm_data.texture_files):
			self.set_dependency_identity(dependency, f"{tex_name}.tex")

	@staticmethod
	def _get_data(file_path):
		fgm_data = FgmFile()
		fgm_data.load(file_path)
		return fgm_data

	def _get_frag_datas(self, fgm_data):
		versions = get_versions(self.ovl)
		sizedstr_bytes = as_bytes(fgm_data.fgm_info, version_info=versions)
		textures_bytes = as_bytes(fgm_data.textures, version_info=versions)
		attributes_bytes = as_bytes(fgm_data.attributes, version_info=versions)
		# todo - this is definitely NOT right/ needed padding by comparing to stock FGMs
		# no clue what the 'rule' here is, it may not be padding but be appear if another pointer is missing
		# textures_bytes += get_padding(len(textures_bytes), alignment=16)
		# attributes never seem to have padding
		# attributes_bytes += get_padding(len(attributes_bytes), alignment=16)
		datas = (textures_bytes, attributes_bytes, fgm_data.data_bytes)
		return datas, sizedstr_bytes

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		buffer_data = self.sized_str_entry.data_entry.buffer_datas[0]

		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:

			with ConvStream() as stream:
				stream.write(self.pack_header(b"FGM "))
				# we need this as its size is not predetermined
				data_lib_f = self.header.data_lib.frag
				data_lib_size = len(data_lib_f.struct_ptr.data) if data_lib_f else 0
				stream.write(struct.pack("II", data_lib_size, len(self.file_entry.dependencies)))
				stream.write(self.sized_str_entry.struct_ptr.data)
				for tex in self.file_entry.dependencies:
					stream.write(zstr(tex.basename.encode()))
				if self.header.textures.data:
					self.header.textures.data.write(stream)
				if self.header.attributes.data:
					self.header.attributes.data.write(stream)
				if data_lib_size:
					stream.write(data_lib_f.struct_ptr.data)
				outfile.write(stream.getvalue())
			# write the buffer
			outfile.write(buffer_data)
		return out_path,

	def _ptrs(self):
		return self.header.textures, self.header.attributes, self.header.data_lib
