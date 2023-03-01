import logging
import io

import numpy as np

from generated.formats.base.compounds.PadAlign import get_padding


from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort


class MemPool(BaseStruct):

	"""
	Description of one archive header entry
	"""

	__name__ = 'MemPool'

	_import_key = 'ovl.compounds.MemPool'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_1 = 0

		# the number of bytes inside this mempool
		self.size = 0

		# byte offset from the start of the mempools region
		self.offset = 0
		self.zero_2 = 0

		# djb2 hash of the first file that points into this mempool
		self.file_hash = 0
		self.disney_zero = 0

		# unknown count (related to number of files or pointers)
		self.num_files = 0

		# JWE: djb2 hash for extension, 0 for PZ
		self.ext_hash = 0
		self.zero_3 = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('zero_1', Uint64, (0, None), (False, None), True),
		('size', Uint, (0, None), (False, None), None),
		('offset', Uint, (0, None), (False, None), None),
		('zero_2', Uint64, (0, None), (False, None), True),
		('file_hash', Uint, (0, None), (False, None), None),
		('disney_zero', Ushort, (0, None), (False, None), True),
		('num_files', Ushort, (0, None), (False, None), True),
		('num_files', Uint, (0, None), (False, None), True),
		('ext_hash', Uint, (0, None), (False, None), True),
		('zero_3', Uint, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 17:
			yield 'zero_1', Uint64, (0, None), (False, None)
		yield 'size', Uint, (0, None), (False, None)
		yield 'offset', Uint, (0, None), (False, None)
		if instance.context.version <= 15:
			yield 'zero_2', Uint64, (0, None), (False, None)
		yield 'file_hash', Uint, (0, None), (False, None)
		if instance.context.version <= 15:
			yield 'disney_zero', Ushort, (0, None), (False, None)
			yield 'num_files', Ushort, (0, None), (False, None)
		if instance.context.version >= 17:
			yield 'num_files', Uint, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint, (0, None), (False, None)
			yield 'zero_3', Uint, (0, None), (False, None)

	def clear_data(self):
		self.new = False
		# lookup by offset
		self.offset_2_struct_entries = {}  # multiple (fragments') struct_ptrs can point to the same data
		self.offset_2_link_entry = {}  # link_ptrs are unique
		self.size_map = {}
		self.offsets = set()
		self.link_offsets = None

	def get_first_offset(self):
		# usually 0, but be safe
		if self.offsets:
			first_offset = sorted(self.offsets)[0]
			return first_offset

	def calc_size_map(self):
		"""Store size of every struct_ptr in size_map"""
		self.size_map = {}
		# sort them
		sorted_offsets = sorted(self.offsets)
		# add the end of the header data block
		sorted_offsets.append(self.size)
		# get the size of each pointer
		for i, offset in enumerate(sorted_offsets[:-1]):
			# get the offset of the next pointer, substract this offset
			data_size = sorted_offsets[i + 1] - offset
			self.size_map[offset] = data_size
		# store array of link offsets for check_for_ptrs
		self.link_offsets = np.array(list(self.offset_2_link_entry.keys()))

	def stream_at(self, offset):
		self.data.seek(offset)
		return self.data

	def get_at(self, offset, size=-1):
		self.data.seek(offset)
		return self.data.read(size)

	def get_data_at(self, offset):
		"""Get data from pool writer"""
		return self.get_at(offset, self.size_map[offset])

	def get_size(self):
		# seek to end of stream
		self.data.seek(0, 2)
		return self.data.tell()

	def pad(self, alignment=4):
		size = self.get_size()
		padding_bytes = get_padding(size, alignment)
		logging.debug(f"Padded pool of ({size} bytes) with {len(padding_bytes)}, alignment = {alignment}")
		self.data.write(padding_bytes)

	def move_empty_pointers_to_end(self):
		end_of_pool = self.get_size()
		# cast to tuple to avoid changing the dict during iteration
		for offset, entries in tuple(self.offset_2_struct_entries.items()):
			if offset != end_of_pool:
				# find any null pointer that is not at the end of the pool
				null_ptrs = [entry for entry in entries if entry.struct_ptr.data_size == 0]
				if null_ptrs:
					logging.debug(f"Moving {len(null_ptrs)} null pointers out of {len(entries)} pointers from {offset} to end of pool at {end_of_pool}")
					# only keep valid pointers at offset
					self.offset_2_struct_entries[offset] = [entry for entry in entries if entry not in null_ptrs]
					# move the null pointers to their new offset
					if end_of_pool not in self.offset_2_struct_entries:
						self.offset_2_struct_entries[end_of_pool] = []
					self.offset_2_struct_entries[end_of_pool].extend(null_ptrs)
					# set data_offset of null_ptrs
					for entry in null_ptrs:
						entry.struct_ptr.data_offset = end_of_pool

	def align_write(self, data, overwrite=False):
		"""Prepares self.pool.data for writing, handling alignment according to type of data"""
		# if overwrite:
		# 	# write at old data_offset, but then check for size match
		# 	if isinstance(data, (bytes, bytearray, str)) and self.data_size != len(data):
		# 		logging.warning(f"Data size for overwritten pointer has changed from {self.data_size} to {len(data)}!")
		# 	self.data.seek(self.data_offset)
		# else:
		# seek to end of pool
		self.data.seek(0, 2)
		# check for alignment
		if isinstance(data, str):
			alignment = 1
		else:
			alignment = 16
		# logging.info(f"{type(data)} {data} alignment {alignment}")
		# write alignment to pool
		if alignment > 1:
			offset = self.data.tell()
			padding = (alignment - (offset % alignment)) % alignment
			if padding:
				self.data.write(b"\x00" * padding)
				logging.debug(
					f"Aligned pointer from {offset} to {self.data.tell()} with {padding} bytes, alignment = {alignment}")
		return self.data, self.data.tell()
		# return True

