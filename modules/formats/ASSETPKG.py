import struct
from modules.formats.shared import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import zstr


class AssetpkgLoader(BaseFile):

	def create(self):
		f_0, f_1 = self._get_data(self.file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		pool.data.write(f_1)
		pool.data.write(f_0)
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool_index = pool_index
		new_frag.pointers[0].data_offset = offset + len(f_1)
		new_frag.pointers[1].pool_index = pool_index
		new_frag.pointers[1].data_offset = offset
		new_ss = self.create_ss_entry(self.file_entry)
		new_ss.pointers[0].pool_index = pool_index
		new_ss.pointers[0].data_offset = offset + len(f_1)

	def collect(self):
		self.assign_ss_entry()
		self.assign_fixed_frags(1)

	def load(self, file_path):
		f_0, f_1 = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(f_1, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print("\nWriting", name)
		f_0 = self.sized_str_entry.fragments[0]
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			f_0.pointers[1].strip_zstring_padding()
			outfile.write(f_0.pointers[1].data[:-1])
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		# copy content, pad to 64b, then assign 1 fragment and 1 empty sized str.
		f_0 = struct.pack('16s', b'')  # fragment pointer 0 data
		f_1 = zstr(self.get_content(file_path))  # fragment pointer 1 data
		return f_0, f_1 + get_padding(len(f_1), alignment=64)
