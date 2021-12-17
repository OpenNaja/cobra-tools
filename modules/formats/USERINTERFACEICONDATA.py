import struct

from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr


class UserinterfaceicondataLoader(BaseFile):

	def create(self):


		ss, f_0, f_1 = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.write_to_pool(self.sized_str_entry.pointers[0], 2, ss)

		# write name and sql as a name ptr each
		f_name, f_package = self.create_fragments(self.sized_str_entry, 2)
		self.ptr_relative(f_name.pointers[0], self.sized_str_entry.pointers[0], rel_offset=0)
		self.write_to_pool(f_name.pointers[1], 2, f"{f_0}".encode('utf-8'))
		self.ptr_relative(f_package.pointers[0], self.sized_str_entry.pointers[0], rel_offset=0x10)
		self.write_to_pool(f_package.pointers[1], 2, f"{f_1}".encode('utf-8'))

	def collect(self):
		self.assign_ss_entry()
		self.assign_fixed_frags(2)

	def load(self, file_path):
		ss, f_01, f_11 = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(f_01, update_copies=True)
		self.sized_str_entry.fragments[1].pointers[1].update_data(f_11, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print("\nWriting", name)
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			for frag in self.sized_str_entry.fragments:
				frag.pointers[1].strip_zstring_padding()
				outfile.write(frag.pointers[1].data[:-1])
				outfile.write(b"\n")
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a USERINTERFACEICON"""
		ss = struct.pack('16s', b'')
		raw_bytes = self.get_content(file_path)
		icname, icpath = [line.strip() for line in raw_bytes.split(b'\n') if line.strip()]
		f_01 = zstr(icname)
		f_02 = zstr(icpath)
		return ss, f_01, f_02 + get_padding(len(f_01) + len(f_02), 64)

