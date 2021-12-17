import struct

from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr


class UserinterfaceicondataLoader(BaseFile):

	def create(self):
		ss, f_01, f_11 = self._get_data(self.file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		# todo - are the 8 bytes needed or just superfluous padding? compare sizes to stock
		pool.data.write(f_01 + f_11 + struct.pack('8s', b''))
		newoffset = pool.data.tell()
		pool.data.write(ss)
		new_frag0 = self.create_fragment()
		new_frag0.pointers[0].pool_index = pool_index
		new_frag0.pointers[0].data_offset = newoffset
		new_frag0.pointers[1].pool_index = pool_index
		new_frag0.pointers[1].data_offset = offset
		new_frag1 = self.create_fragment()
		new_frag1.pointers[0].pool_index = pool_index
		new_frag1.pointers[0].data_offset = newoffset + 8
		new_frag1.pointers[1].pool_index = pool_index
		new_frag1.pointers[1].data_offset = offset + len(f_01)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = newoffset

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
		"""Loads and returns the data for a LUA"""
		ss = struct.pack('16s', b'')
		raw_bytes = self.get_content(file_path)
		icname, icpath = [line.strip() for line in raw_bytes.split(b'\n') if line.strip()]
		f_01 = zstr(icname)
		f_11 = zstr(icpath)
		return ss, f_01, f_11 + get_padding(len(f_01) + len(f_11), 64)

