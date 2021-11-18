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
		pass

	def collect(self):
		self.assign_ss_entry()
		fgm_header = self.sized_str_entry.pointers[0].load_as(FgmHeader)[0]
		frag_count = 2
		if fgm_header.texture_count:
			frag_count += 1
		if self.file_entry.dependencies:
			frag_count += 1
		self.assign_fixed_frags(frag_count)

		# basic fgms - zeros is the ptr to the dependencies block, which is only present if they are present
		if len(self.sized_str_entry.fragments) == 4:
			self.tex_info, self.attr_info, self.zeros, self.data_lib = self.sized_str_entry.fragments
		# no zeros, otherwise same as basic
		elif len(self.sized_str_entry.fragments) == 3:
			self.tex_info, self.attr_info, self.data_lib = self.sized_str_entry.fragments
		# fgms for variants
		elif len(self.sized_str_entry.fragments) == 2:
			self.attr_info, self.data_lib = self.sized_str_entry.fragments
			self.tex_info = None
		else:
			raise AttributeError("Fgm length is wrong")

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

	def load(self, file_path):
		texture_files, datas, sizedstr_bytes, buffer_bytes = self._get_data(file_path)

		self.sized_str_entry.data_entry.update_data((buffer_bytes,))
		self.sized_str_entry.pointers[0].update_data(sizedstr_bytes, update_copies=True)

		# inject fragment datas
		for frag, data in zip(self.sized_str_entry.fragments, datas):
			frag.pointers[1].update_data(data, update_copies=True)

		# update dependencies on ovl
		for dep_entry, tex_name in zip(self.file_entry.dependencies, texture_files):
			dep_entry.basename = tex_name
			dep_entry.name = dep_entry.basename + dep_entry.ext.replace(":", ".")
			dep_entry.file_hash = djb(tex_name.lower())

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
		if len(self.sized_str_entry.fragments) == 4:
			deps_region = self.sized_str_entry.fragments[2]
			datas = (textures_bytes, attributes_bytes, deps_region.pointers[1].data, fgm_data.data_bytes)
		# fgms without dependencies
		elif len(self.sized_str_entry.fragments) == 3:
			datas = (textures_bytes, attributes_bytes, fgm_data.data_bytes)
		# fgms for variants
		elif len(self.sized_str_entry.fragments) == 2:
			datas = (attributes_bytes, fgm_data.data_bytes)
			# we have some additional bytes here
			sizedstr_bytes += b"\x00" * 8
		else:
			raise AttributeError("Unexpected fgm frag count")
		return fgm_data.texture_files, datas, sizedstr_bytes, fgm_data.buffer_bytes

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		buffer_data = self.sized_str_entry.data_entry.buffer_datas[0]

		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(self.pack_header(b"FGM "))
			# we need this as its size is not predetermined
			outfile.write(struct.pack("II", len(self.data_lib.pointers[1].data), len(self.file_entry.dependencies)))
			# if there are 2 fragments, it is 24 bytes instead of 16
			outfile.write(self.sized_str_entry.pointers[0].data[:16])
			for tex in self.file_entry.dependencies:
				outfile.write(zstr(tex.basename.encode()))
			# write each of the fragments
			for frag in (self.tex_info, self.attr_info, self.data_lib):
				if frag:
					outfile.write(frag.pointers[1].data)
			# write the buffer
			outfile.write(buffer_data)
		return out_path,
