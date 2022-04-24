import logging

from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr


class UserinterfaceicondataLoader(BaseFile):
	extension = ".userinterfaceicondata"

	def create(self):
		f_01, f_11 = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		frag0, frag1 = self.create_fragments(self.sized_str_entry, 2)
		ss_ptr = self.sized_str_entry.pointers[0]
		self.write_to_pool(ss_ptr, 2, b"\x00" * 16)
		self.ptr_relative(frag0.pointers[0], ss_ptr)
		self.ptr_relative(frag1.pointers[0], ss_ptr, rel_offset=8)
		self.write_to_pool(frag0.pointers[1], 2, f_01)
		self.write_to_pool(frag1.pointers[1], 2, f_11)

	def collect(self):
		self.assign_ss_entry()
		self.assign_fixed_frags(2)

	def load(self, file_path):
		f_01, f_11 = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(f_01, update_copies=True)
		self.sized_str_entry.fragments[1].pointers[1].update_data(f_11, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		with open(out_path, 'w') as outfile:
			for frag in self.sized_str_entry.fragments:
				outfile.write(self.p1_ztsr(frag))
				outfile.write("\n")
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a LUA"""
		raw_bytes = self.get_content(file_path)
		icname, icpath = [line.strip() for line in raw_bytes.split(b'\n') if line.strip()]
		f_01 = zstr(icname)
		f_11 = zstr(icpath)
		return f_01, f_11 + get_padding(len(f_01) + len(f_11), 64)

