
import logging
import io

from generated.io import BinaryStream
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

		logging.debug(f"Flushing ptrs")
		# first, get all ptrs that have data to write
		sorted_ptrs_map = sorted(self.pointer_map.items())

		stack = []
		last_offset = -1
		for i, (offset, pointers) in enumerate(sorted_ptrs_map):
			for ptr in pointers:
				if ptr._data is not None:
					if last_offset == offset:
						logging.warning(f"last offset is same as offset {offset}, skipping ptr for update")
						continue
					stack.append((ptr, i, offset))
					last_offset = offset

		# check if rewriting is needed
		if not stack:
			return
		# create new data writer
		data = BinaryStream()
		last_offset = 0
		# now go sequentially over all ptrs in the stack
		for ptr, i, offset in stack:
			from_end_of_last_to_start_of_this = self.get_at(last_offset, size=offset-last_offset)
			# write old data before this chunk and new data
			data.write(from_end_of_last_to_start_of_this)
			logging.debug(f"Flushing stack member {i} at original offset {offset} to {data.tell()}")

			data.write(ptr._data)
			# update offset to end of the original ptr
			last_offset = offset + ptr.data_size
			# check delta
			# todo - padding
			ptr._padding_size = ptr.padding_size
			delta = (len(ptr._data) + ptr._padding_size) - (ptr.data_size + ptr.padding_size)
			# update new data size on ptr
			ptr.data_size = len(ptr._data)
			if delta:
				# logging.debug(f"data size of stack [len: {len(sorted_ptrs_map)}] member {i} has changed")
				# get all ptrs that point into this pool, but after this ptr
				if i < len(sorted_ptrs_map):
					for offset_later, pointers in sorted_ptrs_map[i+1:]:
						# logging.debug(f"Moving {offset_later} to {offset_later+delta}")
						# update their data offsets
						for p in pointers:
							p.data_offset += delta
			# todo - remove from ptr map or force regenerating it each time
			# if self.data_offset in self.pool.pointer_map:
			# 	ptrs = self.pool.pointer_map[self.data_offset]
			# 	ptrs.remove(self)
			# 	if not ptrs:
			# 		self.pool.pointer_map.pop(self.data_offset)
		# write the rest of the data
		data.write(self.get_at(last_offset))
		# clear ptr data and stack
		for ptr, i, offset in stack:
			ptr._data = None
		# overwrite internal data
		self.data = data

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
		# calculate pointer data sizes
		# make them unique and sort them
		sorted_items = sorted(self.pointer_map.items())
		# pick all ptrs except frag ptr0
		sorted_items_filtered = [(offset, pointers) for offset, pointers in sorted_items if any(p.is_ref_ptr for p in pointers)]
		# logging.info(f"len(sorted_items) {len(sorted_items)}, len(sorted_items_filtered) {len(sorted_items_filtered)}")
		# add the end of the header data block
		sorted_items_filtered.append((self.size, None))
		# get the size of each pointer
		for i, (offset, pointers) in enumerate(sorted_items_filtered[:-1]):
			# get the offset of the next pointer, substract this offset
			data_size = sorted_items_filtered[i + 1][0] - offset
			for pointer in pointers:
				pointer.data_size = data_size

	def get_at(self, offset, size=-1):
		self.data.seek(offset)
		return self.data.read(size)

	def get_size(self):
		# seek to end of stream
		self.data.seek(0, 2)
		return self.data.tell()

	def pad(self, alignment=4):
		size = self.get_size()
		padding_bytes = get_padding(size, alignment)
		logging.debug(f"Padded pool of ({size} bytes) with {len(padding_bytes)}, alignment = {alignment}")
		self.data.write(padding_bytes)

