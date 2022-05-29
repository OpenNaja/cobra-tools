import struct
from generated.formats.ovl.versions import is_dla
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding


class TxtLoader(BaseFile):
	extension = ".txt"

	def create(self):
		self.root_entry = self.create_root_entry(self.file_entry)
		self.root_entry.struct_ptr.pool.num_files += 1
		self.write_data_to_pool(self.root_entry.struct_ptr, 2, self._get_data(self.file_entry.path))

	def extract(self, out_dir, show_temp_files, progress_callback):
		b = self.root_entry.struct_ptr.data
		if is_dla(self.ovl):
			# not sure, not standard sized strings
			size, unk = struct.unpack("<2B", b[:2])
			data = b[2:2+size*2]
		else:
			size = struct.unpack("<I", b[:4])[0]
			data = b[4:4+size]
		out_path = out_dir(self.root_entry.name)
		with open(out_path, "wb") as f:
			f.write(data)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		raw_txt_bytes = self.get_content(file_path)
		root_entry = struct.pack("<I", len(raw_txt_bytes)) + raw_txt_bytes + b"\x00"
		return root_entry + get_padding(len(root_entry), alignment=8)
