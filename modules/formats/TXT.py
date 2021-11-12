import struct
from generated.formats.ovl.versions import is_dla
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding


class TxtLoader(BaseFile):

	def create(self):
		ss = self._get_data(self.file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = offset
		pool.data.write(ss)
		pool.num_files += 1

	def collect(self):
		self.assign_ss_entry()
	
	def load(self, file_path):
		ss = self._get_data(file_path)
		self.sized_str_entry.pointers[0].update_data(ss, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		b = self.sized_str_entry.pointers[0].data
		if is_dla(self.ovl):
			# not sure, not standard sized strings
			size, unk = struct.unpack("<2B", b[:2])
			data = b[2:2+size*2]
		else:
			size = struct.unpack("<I", b[:4])[0]
			data = b[4:4+size]
		out_path = out_dir(self.sized_str_entry.name)
		with open(out_path, "wb") as f:
			f.write(data)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		raw_txt_bytes = self.get_content(file_path)
		ss = struct.pack("<I", len(raw_txt_bytes)) + raw_txt_bytes + b"\x00"
		return ss + get_padding(len(ss), alignment=8)
