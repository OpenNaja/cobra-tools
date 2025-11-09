import contextlib
import logging
import os
import struct
import time
import re
from pathlib import Path


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])


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
