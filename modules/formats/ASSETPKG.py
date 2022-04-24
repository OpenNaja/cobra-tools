import logging
from modules.formats.shared import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import zstr


class AssetpkgLoader(BaseFile):
	extension = ".assetpkg"

	def create(self):
		ss, f_1 = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		f = self.create_fragments(self.sized_str_entry, 1)[0]
		self.write_to_pool(f.pointers[1], 2, f_1)
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, ss)
		self.ptr_relative(f.pointers[0], self.sized_str_entry.pointers[0])

	def collect(self):
		self.assign_ss_entry()
		self.assign_fixed_frags(1)

	def load(self, file_path):
		ss, f_1 = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(f_1, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		with open(out_path, 'w') as outfile:
			outfile.write(self.p1_ztsr(self.sized_str_entry.fragments[0]))
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		# copy content, pad to 64b, then assign 1 fragment and 1 empty sized str.
		ss = b"\x00" * 16  # 1 ptr, 8 unused bytes
		f_1 = zstr(self.get_content(file_path))  # fragment pointer 1 data
		return ss, f_1 + get_padding(len(f_1), alignment=64)
