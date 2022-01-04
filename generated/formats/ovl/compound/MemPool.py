
import logging
import io
from modules.formats.shared import get_padding


from generated.context import ContextReference


class MemPool:

	"""
	Description of one archive header entry
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# always 0
		self.zero_1 = 0

		# the number of bytes inside this mempool
		self.size = 0

		# byte offset from the start of the mempools region
		self.offset = 0

		# always 0
		self.zero_2 = 0

		# DJB hash of the first file that points into this mempool
		self.file_hash = 0

		# unknown count (related to number of files or pointers)
		self.num_files = 0

		# JWE: DJB hash for extension, 0 for PZ
		self.ext_hash = 0

		# always 0
		self.zero_3 = 0
		self.set_defaults()

	def set_defaults(self):
		if not (self.context.version == 15):
			self.zero_1 = 0
		self.size = 0
		self.offset = 0
		if self.context.version == 15:
			self.zero_2 = 0
		self.file_hash = 0
		self.num_files = 0
		if self.context.version >= 19:
			self.ext_hash = 0
		if self.context.version >= 19:
			self.zero_3 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		if not (self.context.version == 15):
			self.zero_1 = stream.read_uint64()
		self.size = stream.read_uint()
		self.offset = stream.read_uint()
		if self.context.version == 15:
			self.zero_2 = stream.read_uint64()
		self.file_hash = stream.read_uint()
		self.num_files = stream.read_uint()
		if self.context.version >= 19:
			self.ext_hash = stream.read_uint()
			self.zero_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		if not (self.context.version == 15):
			stream.write_uint64(self.zero_1)
		stream.write_uint(self.size)
		stream.write_uint(self.offset)
		if self.context.version == 15:
			stream.write_uint64(self.zero_2)
		stream.write_uint(self.file_hash)
		stream.write_uint(self.num_files)
		if self.context.version >= 19:
			stream.write_uint(self.ext_hash)
			stream.write_uint(self.zero_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* num_files = {self.num_files.__repr__()}'
		s += f'\n	* ext_hash = {self.ext_hash.__repr__()}'
		s += f'\n	* zero_3 = {self.zero_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def flush_pointers(self, ignore_unaccounted_bytes=False):
		"""Pre-writing step to convert all edits that were done on individual pointers back into the consolidated header
		data io block"""
		if self.update_from_ptrs:
			# maintain sorting order
			# grab the first pointer for each address
			# it is assumed that subsequent pointers to that address share the same data
			sorted_first_pointers = [pointers[0] for offset, pointers in sorted(self.pointer_map.items())]
			if sorted_first_pointers:
				# only known from indominus
				first_offset = sorted_first_pointers[0].data_offset
				if first_offset != 0 and not ignore_unaccounted_bytes:
					logging.debug(f"Found {first_offset} unaccounted bytes at start of pool")
					unaccounted_bytes = self.data.getvalue()[:first_offset]
				else:
					unaccounted_bytes = b""

				# clear io objects
				self.data = io.BytesIO()
				self.data.write(unaccounted_bytes)
				# write updated strings
				for pointer in sorted_first_pointers:
					pointer.write_data(update_copies=True)
			else:
				# todo - shouldn't we delete the pool in that case?
				logging.debug(f"No pointers into pool {self.offset} - keeping its stock data!")

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
		# calculate pointer data sizes
		# make them unique and sort them
		sorted_items = sorted(self.pointer_map.items())
		# add the end of the header data block
		sorted_items.append((self.size, None))
		# get the size of each pointer
		for i, (offset, pointers) in enumerate(sorted_items[:-1]):
			# get the offset of the next pointer, substract this offset
			data_size = sorted_items[i + 1][0] - offset
			for pointer in pointers:
				pointer.data_size = data_size
				pointer.copies = pointers
				pointer.read_data()

	def pad(self, alignment=4):
		if self.update_from_ptrs:
			self.data.write(get_padding(self.data.tell(), alignment))

