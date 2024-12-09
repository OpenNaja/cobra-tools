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

	@property
	def encoding(self):
		if self.mime_version == 1:
			return UTF16
		else:
			return UTF8

	def extract(self, out_dir):
		pool, offset = self.root_ptr
		b = pool.get_data_at(offset)
		# sized strings
		if self.mime_version == 1:
			# DLA uses utf16, so every second byte is 00, eg b'C\x00a\x00m\x00e\x00r\x00a\x00'
			char_count, count_mask = struct.unpack("<2B", b[:2])
			# count_mask's first bit is always on
			# 128 ~ 0b10000000 ~ no additional
			# 129 ~ 0b10000001 ~ 1*256 additional chars
			count_mask &= 0b01111111
			data = b[2:2+(char_count+256*count_mask)*2]
		elif self.mime_version in (2, 3):
			# version 2 (PC1, JWE1) & 3 (PZ, JWE2, WH)
			char_count = struct.unpack("<I", b[:4])[0]
			data = b[4:4+char_count]
		elif self.mime_version == 4:
			# PC2
			char_count = struct.unpack("<Q", b[:8])[0]
			data = b[8:8+char_count]
		else:
			raise AttributeError(f"Unknown TXT format {self.mime_version}")
		out_path = out_dir(self.name)
		with open(out_path, "w", encoding=UTF8) as f:
			f.write(data.decode(self.encoding))
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a TXT"""
		with open(file_path, 'r', encoding=UTF8) as f:
			txt_str = f.read()
		txt_bytes = txt_str.encode(self.encoding)
		if self.mime_version == 1:
			# take char count, not byte count
			len_raw = len(txt_str)
			len_div = len_raw // 256
			len_mod = len_raw % 256
			len_div |= 0b10000000  # set first bit to 1
			prefix = struct.pack("<2B", len_mod, len_div)
		elif self.mime_version in (2, 3):
			prefix = struct.pack("<I", len(txt_bytes))
		elif self.mime_version == 4:
			prefix = struct.pack("<Q", len(txt_bytes))
		else:
			raise AttributeError(f"Unknown TXT format {self.mime_version}")
		root_entry = prefix + txt_bytes + b"\x00"
		return root_entry + get_padding(len(root_entry), alignment=8)
