import struct
from generated.formats.base.compounds.PadAlign import get_padding
from generated.formats.ovl.versions import is_dla
from modules.formats.BaseFormat import BaseFile


class TxtLoader(BaseFile):
	extension = ".txt"

	def create(self, file_path):
		self.write_root_bytes(self._get_data(file_path))
		pool, offset = self.root_ptr
		pool.num_files += 1

	def extract(self, out_dir):
		pool, offset = self.root_ptr
		b = pool.get_data_at(offset)
		# sized strings
		if self.mime_version == 1:
			# DLA
			# unk = 128, usually
			size, unk = struct.unpack("<2B", b[:2])
			data = b[2:2+size*2]
		elif self.mime_version >= 4:
			# PC2
			size = struct.unpack("<Q", b[:8])[0]
			data = b[8:8+size]
		else:
			# version 2 (PC1, JWE1) & 3 (PZ, JWE2, WH)
			size = struct.unpack("<I", b[:4])[0]
			data = b[4:4+size]
		out_path = out_dir(self.name)
		with open(out_path, "wb") as f:
			f.write(data)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		raw_txt_bytes = self.get_content(file_path)
		fmt = "<I" if self.mime_version in (2, 3) else "<Q"
		root_entry = struct.pack(fmt, len(raw_txt_bytes)) + raw_txt_bytes + b"\x00"
		return root_entry + get_padding(len(root_entry), alignment=8)
