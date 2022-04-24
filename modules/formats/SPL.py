import logging
import struct
from modules.formats.shared import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import zstr


class SplineLoader(BaseFile):
	extension = ".spl"

	def create(self):
		if True:
			pass
		f_0, f_1 = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		f = self.create_fragments(self.sized_str_entry, 1)[0]
		self.write_to_pool(f.pointers[1], 2, f_1)
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, b"")
		self.write_to_pool(f.pointers[0], 4, f_0)

	def collect(self):
		if True:
			pass
		self.assign_ss_entry()
		self.assign_fixed_frags(1)

	def load(self, file_path):
		if True:
			pass
		f_0, f_1 = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(f_1, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		if True:
			pass
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		f_0 = self.sized_str_entry.fragments[0]
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			f_0.pointers[1].strip_zstring_padding()
			outfile.write(f_0.pointers[1].data[:-1])
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a CURVE"""
		# copy content, pad to 64b, then assign 1 fragment and 1 empty sized str.
		f_0 = struct.pack('16s', b'')  # fragment pointer 0 data
		f_1 = zstr(self.get_content(file_path))  # fragment pointer 1 data
		return f_0, f_1 + get_padding(len(f_1), alignment=64)
