import struct
from generated.formats.base.compounds.PadAlign import get_padding
from generated.formats.ovl.versions import is_dla
from modules.formats.BaseFormat import BaseFile


class TxtLoader(BaseFile):
	extension = ".txt"

	def create(self, file_path):
		self.create_root_entry()
		self.write_data_to_pool(self.root_entry.struct_ptr, 2, self._get_data(file_path))
		self.root_entry.struct_ptr.pool.num_files += 1

	def extract(self, out_dir):
		b = self.root_entry.struct_ptr.data
		if is_dla(self.ovl):
			# not sure, not standard sized strings
			size, unk = struct.unpack("<2B", b[:2])
			data = b[2:2+size*2]
		else:
			size = struct.unpack("<I", b[:4])[0]
			data = b[4:4+size]
		out_path = out_dir(self.name)
		with open(out_path, "wb") as f:
			f.write(data)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		raw_txt_bytes = self.get_content(file_path)
		root_entry = struct.pack("<I", len(raw_txt_bytes)) + raw_txt_bytes + b"\x00"
		return root_entry + get_padding(len(root_entry), alignment=8)
