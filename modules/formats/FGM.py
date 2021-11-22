import logging
import struct

from generated.formats.fgm.compound.FgmHeader import FgmHeader
from generated.formats.ovl_base.versions import is_ztuac
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_versions, djb, get_padding
from modules.helpers import as_bytes, zstr
from generated.formats.fgm import FgmFile


class FgmLoader(BaseFile):

	def create(self):

		fgm_data, datas, sizedstr_bytes = self._get_data(self.file_entry.path)
		# first create dependencies
		for tex_name in fgm_data.texture_files:
			self.create_dependency(f"{tex_name}.tex")
		# now check for frags
		frag_count = self._get_frag_count(fgm_data.fgm_info)
		# JWE2 patternset fgms seem to be in pool type 3, everything else in 2
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()

		# all ss + ptr 0 frag data
		pool.data.write(sizedstr_bytes + get_padding(len(sizedstr_bytes), alignment=64))

		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = offset
		self.create_data_entry(self.sized_str_entry, (fgm_data.buffer_bytes,))

		for frag_i in range(frag_count):
			frag = self.create_fragment()
			self.sized_str_entry.fragments.append(frag)
		self._tag_fragments(fgm_data.fgm_info)

		# these are eyeballed, not sure if they will work
		if frag_count == 2:
			offsets = (24, 50)
		elif frag_count == 3:
			offsets = (16, 24, 32)
		elif frag_count == 4:
			offsets = (16, 24, 32, 40)
		for frag, rel_offset in zip(self.sized_str_entry.fragments, offsets):
			frag.pointers[0].pool_index = pool_index
			frag.pointers[0].data_offset = offset + rel_offset

		# write the actual data
		for frag, data in zip(self._valid_frags(), datas):
			frag.pointers[1].pool_index = pool_index
			frag.pointers[1].data_offset = pool.data.tell()
			pool.data.write(data)

		if fgm_data.texture_files:
			# points to the start of the dependencies region
			self.dependencies_ptr.pointers[1].data_offset = pool.data.tell()
			for dependency in self.file_entry.dependencies:
				dependency.pointers[0].data_offset = pool.data.tell()
				# todo - check size for dependency pointers, IIRC it varies
				pool.data.write(b"\x00" * 8)

	def collect(self):
		self.assign_ss_entry()
		fgm_header = self.sized_str_entry.pointers[0].load_as(FgmHeader)[0]
		frag_count = self._get_frag_count(fgm_header)
		logging.debug(f"FGM: {self.sized_str_entry.name} {frag_count}")
		self.assign_fixed_frags(frag_count)

		self._tag_fragments(fgm_header)

		if self.tex_info:
			# size of a texture info varies
			if is_ztuac(self.ovl):
				tex_size = fgm_header.texture_count * 12
			else:
				tex_size = fgm_header.texture_count * 24
			self.tex_info.pointers[1].split_data_padding(tex_size)
		# this likely has no padding anyway
		self.attr_info.pointers[1].split_data_padding(fgm_header.attribute_count * 16)
		for i, f in enumerate(self.sized_str_entry.fragments):
			p = f.pointers[1]
			logging.debug(f"{self.sized_str_entry.name} {i} {len(p.data)} {len(p.padding)}")

	def _tag_fragments(self, fgm_header):
		logging.info(f"Tagging {len(self.sized_str_entry.fragments)} fragments")
		# basic fgms - zeros is the ptr to the dependencies block, which is only present if they are present
		if fgm_header.attribute_count and fgm_header.texture_count and self.file_entry.dependencies:
			self.tex_info, self.attr_info, self.dependencies_ptr, self.data_lib = self.sized_str_entry.fragments
		# no dependencies_ptr, otherwise same as basic
		elif fgm_header.attribute_count and fgm_header.texture_count:
			self.tex_info, self.attr_info, self.data_lib = self.sized_str_entry.fragments
		# fgms for variants
		elif fgm_header.attribute_count:
			self.attr_info, self.data_lib = self.sized_str_entry.fragments
			self.tex_info = None
		# fgms for patternset
		elif fgm_header.texture_count:
			self.tex_info, self.dependencies_ptr = self.sized_str_entry.fragments
			self.attr_info = None
			self.data_lib = None
		else:
			raise AttributeError("Fgm length is wrong")

	def _get_frag_count(self, fgm_header):
		frag_count = 0
		if fgm_header.texture_count:
			frag_count += 1
		if fgm_header.attribute_count:
			# attrib + data frag
			frag_count += 2
		if self.file_entry.dependencies:
			frag_count += 1
		return frag_count

	def load(self, file_path):
		fgm_data, datas, sizedstr_bytes = self._get_data(file_path)

		self.sized_str_entry.data_entry.update_data((fgm_data.buffer_bytes,))
		self.sized_str_entry.pointers[0].update_data(sizedstr_bytes, update_copies=True)

		# inject fragment datas
		for frag, data in zip(self._valid_frags(), datas):
			frag.pointers[1].update_data(data, update_copies=True)

		# update dependencies on ovl
		for dependency, tex_name in zip(self.file_entry.dependencies, fgm_data.texture_files):
			self.set_dependency_identity(dependency, f"{tex_name}.tex")

	def _get_data(self, file_path):
		versions = get_versions(self.ovl)
		fgm_data = FgmFile()
		fgm_data.load(file_path)
		sizedstr_bytes = as_bytes(fgm_data.fgm_info, version_info=versions)
		textures_bytes = as_bytes(fgm_data.textures, version_info=versions)
		attributes_bytes = as_bytes(fgm_data.attributes, version_info=versions)
		# todo - verify this is the right / needed padding by comparing to stock FGMs
		textures_bytes += get_padding(len(textures_bytes), alignment=16)
		attributes_bytes += get_padding(len(attributes_bytes), alignment=16)
		frag_count = self._get_frag_count(fgm_data.fgm_info)
		if frag_count == 4:
			# todo - somehow handle the pointers - we don't know their size before
			deps_region = self.sized_str_entry.fragments[2]
			datas = (textures_bytes, attributes_bytes, fgm_data.data_bytes)
		# fgms without dependencies
		elif frag_count == 3:
			datas = (textures_bytes, attributes_bytes, fgm_data.data_bytes)
		# fgms for variants
		elif frag_count == 2:
			datas = (attributes_bytes, fgm_data.data_bytes)
			# we have some additional bytes here
			sizedstr_bytes += b"\x00" * 8
		else:
			raise AttributeError("Unexpected fgm frag count")
		return fgm_data, datas, sizedstr_bytes

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		buffer_data = self.sized_str_entry.data_entry.buffer_datas[0]

		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(self.pack_header(b"FGM "))
			# we need this as its size is not predetermined
			data_lib_size = len(self.data_lib.pointers[1].data) if self.data_lib else 0
			outfile.write(struct.pack("II", data_lib_size, len(self.file_entry.dependencies)))
			# if there are 2 fragments, it is 24 bytes instead of 16
			outfile.write(self.sized_str_entry.pointers[0].data[:16])
			for tex in self.file_entry.dependencies:
				outfile.write(zstr(tex.basename.encode()))
			# write each of the fragments
			for frag in self._valid_frags():
				outfile.write(frag.pointers[1].data)
			# write the buffer
			outfile.write(buffer_data)
		return out_path,

	def _valid_frags(self):
		"""Only yields fragments with data, ignores dependency pointers fragment and missing fragments"""
		for frag in (self.tex_info, self.attr_info, self.data_lib):
			if frag:
				yield frag
