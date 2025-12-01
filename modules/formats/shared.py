import contextlib
import logging
import os
import io
import struct
import time
import re
from pathlib import Path
from typing import Any, Generator, LiteralString, Iterable


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])


TAB = '  '


def hex_dump(data: str | bytes | Iterable[int], show_offset=True, show_txt=True,
			 indent=0, offset=0, line_width=16, encoding="latin-1") -> str:
	"""
	Pretty-prints a sequence in hex dump format.

	Args:
		data: The sequence to be printed.
	"""
	if isinstance(data, str):
		data = bytearray(data, encoding)
	else:
		data = bytearray(data)

	hex_format: LiteralString = " ".join(["{:02X}" for _ in range(line_width)])
	output = io.StringIO()
	for i in range(0, len(data), line_width):
		# Must pad to line width for format string
		line_data: bytearray = data[i:i + line_width].ljust(line_width, b'\x00')
		txt_line: str = ""
		offset_line: str = ""
		# Show text column
		if show_txt:
			for c in line_data:
				c: str = chr(c)
				txt_line += c if c.isprintable() else "."
			txt_line = f"  {txt_line}"
		# Show offset column
		if show_offset:
			offset_line = f"{i + offset:08X}  "
		output.write(f"{indent * TAB}{offset_line}{hex_format.format(*line_data)}{txt_line}\n")
	return output.getvalue()


def hex_dump_generator(in_file: io.BufferedReader, show_offset=True, show_txt=True,
					   indent=0, offset=0, line_width=16) -> Generator[str, Any, None]:
	"""
	Pretty-prints a file in hex dump format.

	Args:
		in_file: A BufferedReader for the input file
	"""
	hex_format: LiteralString = " ".join(["{:02X}" for _ in range(line_width)])
	offset: int = offset
	while True:
		data: bytes = in_file.read(line_width)
		if not data:
			break

		# Must pad to line width for format string
		line_data: bytes = data.ljust(line_width, b'\x00')
		txt_line: str = ""
		offset_line: str = ""
		# Show text column
		if show_txt:
			for c in line_data:
				c: str = chr(c)
				txt_line += c if c.isprintable() else "."
			txt_line = f"  {txt_line}"
		# Show offset column
		if show_offset:
			offset_line = f"{offset:08X}  "
		yield f"{indent * TAB}{offset_line}{hex_format.format(*line_data)}{txt_line}\n"

		offset += line_width


def splitext_safe(fp: str) -> tuple[str, str]:
	# os.path.splitext fails on /ymaiotriqnd03i9/.texel
	# i.e. ('/ymaiotriqnd03i9/.texel', '')
	if "." in fp:
		name, ext = fp.rsplit(".", 1)
		return name, f".{ext}"
	# No dot found, so no extension
	return fp, ""


def get_padding_size(size, alignment=16):
	mod = size % alignment
	if mod:
		return alignment - mod
	return 0


def get_padding(size, alignment=16):
	if alignment:
		# create the new blank padding
		return b"\x00" * get_padding_size(size, alignment=alignment)
	return b""


def djb2(s: str):
	"""calculates djb2 hash for string s"""
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	n = 5381
	for x in s:
		n = ((n << 5) + n) + ord(x)
	return n & 0xFFFFFFFF


def fnv1_32(b: bytes):
	"""calculates fnv1 (32 bit) hash for bytes b"""
	# adapted from https://github.com/znerol/py-fnvhash/blob/main/fnvhash/__init__.py
	assert isinstance(b, bytes)
	n = 0x811c9dc5
	for byte in b:
		n = (n * 0x01000193) % (2**32)
		n = n ^ byte
	return n


alphanum = re.compile(r"[^0-9A-Za-z]", re.IGNORECASE)


def hash_guid(guid_str: str) -> int:
	# Remove all non-alphanumeric characters
	filtered = alphanum.sub("", guid_str)

	# Mixed-endian byte order
	byte_order = [3, 2, 1, 0, 5, 4, 7, 6, 8, 9, 10, 11, 12, 13, 14, 15]

	# Convert the reordered hex pairs to bytes
	guid_bytes = bytearray()
	for i in byte_order:
		hex_pair = filtered[i * 2:i * 2 + 2]
		guid_bytes.append(int(hex_pair, 16))

	mask = 1073741823  # Bitmask for first 30 bits
	hash_32 = fnv1_32(guid_bytes)
	return (hash_32 >> 30) ^ (hash_32 & mask)  # XOR folding


def fnv64(b: bytes):
	"""calculates fnv64 hash for bytes b"""
	n = 0xcbf29ce484222325
	for byte in b:
		n *= 0x100000001b3
		n &= 0xffffffffffffffff
		n ^= byte
	return n


def encode_int64_base32(integer: int, charset: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"):
	"""Encodes a 64-bit integer into a base32 string with a custom charset."""
	encoded = ""
	for _ in range(13):
		index = integer & 0x1F
		encoded += charset[index]
		integer >>= 5
	return encoded


def fmt_hash(id_hash):
	return "".join([f"{b:02X}" for b in struct.pack("<I", id_hash)])


class DummySignal:

	def emit(self, val):
		pass
	# logging.debug(f"Emitted {val}")

	def connect(self, func):
		pass


class DummyReporter:
	"""A class wrapping the interaction between OvlFile and the UI"""
	warning_msg = DummySignal()  # type: ignore
	success_msg = DummySignal()  # type: ignore
	files_list = DummySignal()  # type: ignore
	included_ovls_list = DummySignal()  # type: ignore
	progress_percentage = DummySignal()  # type: ignore
	progress_total = DummySignal()  # type: ignore
	current_action = DummySignal()  # type: ignore

	def iter_progress(self, iterable, message, cond=True):
		if cond:
			self.current_action.emit(message)
			self._percentage = -1
			if len(iterable) > 1:
				self.progress_total.emit(100)
			else:
				self.progress_total.emit(0)
			for i, item in enumerate(iterable):
				p = round(i / len(iterable) * 100)
				if p != self._percentage:
					self.progress_percentage.emit(p)
					self._percentage = p
				yield item
			# clear both to also make indeterminate processes appear complete
			self.progress_percentage.emit(100)
			self.progress_total.emit(100)
			msg = f"Finished {message}"
			self.current_action.emit(msg)
		# logging.success(msg)
		else:
			for item in iterable:
				yield item

	@contextlib.contextmanager
	def report_error_files(self, operation):
		error_files = []
		yield error_files
		if error_files:
			self.warning_msg.emit(
				(f"{operation} {len(error_files)} files failed - please check 'Show Details' or the log.",
				 "\n".join(error_files)))
		else:
			msg = f"{operation} succeeded"
			logging.success(msg)
			self.success_msg.emit(msg)

	def show_success(self, msg):
		logging.success(msg)
		self.success_msg.emit(msg)

	def show_error(self, msg, files=()):
		self.warning_msg.emit((msg, "\n".join(files)))

	@contextlib.contextmanager
	def log_duration(self, operation):
		logging.info(operation)
		start_time = time.time()
		yield
		duration = time.time() - start_time
		logging.debug(f"{operation} took {duration:.2f} seconds")


def walk_type(start_dir, extension=".ovl"):
	logging.info(f"Scanning {Path(start_dir)} for {extension} files")
	ret = []
	for root, dirs, files in os.walk(start_dir, topdown=False):
		for name in files:
			if extension and not name.lower().endswith(extension):
				continue
			ret.append(os.path.normpath(os.path.join(root, name)))
	return ret


filepath_escapes = {
	"|": "&#124;",
}


def escape_path(filepath):
	for k, v in filepath_escapes.items():
		filepath = filepath.replace(k, v)
	return filepath


def unescape_path(filepath):
	for k, v in filepath_escapes.items():
		filepath = filepath.replace(v, k)
	return filepath


def make_out_dir_func(out_dir):
	def out_dir_func(n):
		"""Helper function to generate temporary output file name"""
		out_path = os.path.normpath(os.path.join(out_dir, escape_path(n)))
		# create output dir
		os.makedirs(os.path.dirname(out_path), exist_ok=True)
		return out_path

	return out_dir_func