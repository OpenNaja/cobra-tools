import struct
from generated.formats.base.compounds.PadAlign import get_padding
from modules.formats.BaseFormat import BaseFile

UTF8 = "utf-8"
UTF16 = "utf-16-le"  # 00 bytes is second


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
			# DLA has every second byte as 00, eg b'C\x00a\x00m\x00e\x00r\x00a\x00'
			# unk = 128, usually
			char_count, unk = struct.unpack("<2B", b[:2])
			data = b[2:2+char_count*2].decode(UTF16)
		elif self.mime_version in (2, 3):
			# version 2 (PC1, JWE1) & 3 (PZ, JWE2, WH)
			char_count = struct.unpack("<I", b[:4])[0]
			data = b[4:4+char_count].decode(UTF8)
		elif self.mime_version == 4:
			# PC2
			char_count = struct.unpack("<Q", b[:8])[0]
			data = b[8:8+char_count].decode(UTF8)
		else:
			raise AttributeError(f"Unknown TXT format {self.mime_version}")
		out_path = out_dir(self.name)
		with open(out_path, "w", encoding=UTF8) as f:
			f.write(data)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		with open(file_path, 'r', encoding=UTF8) as f:
			txt_str = f.read()
		if self.mime_version == 1:
			txt_bytes = txt_str.encode(UTF16)
			prefix = struct.pack("<2B", len(txt_str), 128)
		elif self.mime_version in (2, 3):
			txt_bytes = txt_str.encode(UTF8)
			prefix = struct.pack("<I", len(txt_str))
		elif self.mime_version == 4:
			txt_bytes = txt_str.encode(UTF8)
			prefix = struct.pack("<Q", len(txt_str))
		else:
			raise AttributeError(f"Unknown TXT format {self.mime_version}")
		root_entry = prefix + txt_bytes + b"\x00"
		return root_entry + get_padding(len(root_entry), alignment=8)
