import logging
import io

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

		# always 0
		self.zero_1 = 0

		# the number of bytes inside this mempool
		self.size = 0

		# byte offset from the start of the mempools region
		self.offset = 0

		# always 0
		self.zero_2 = 0

		# djb2 hash of the first file that points into this mempool
		self.file_hash = 0

		# zero
		self.disney_zero = 0

		# unknown count (related to number of files or pointers)
		self.num_files = 0

		# JWE: djb2 hash for extension, 0 for PZ
		self.ext_hash = 0

		# always 0
		self.zero_3 = 0
		if set_default:
			self.set_defaults()

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

	def get_first_entry(self):
		# usually 0, but be safe
		if self.offset_2_struct_entries:
			first_offset = sorted(self.offset_2_struct_entries.keys())[0]
			first_entries = self.offset_2_struct_entries[first_offset]
			if first_entries:
				return first_entries[0]

	def calc_struct_ptr_sizes(self):
		"""Assign an estimated size to every struct_ptr"""
		# sort them
		sorted_entries = sorted(self.offset_2_struct_entries.items())
		# add the end of the header data block
		sorted_entries.append((self.size, None))
		# get the size of each pointer
		for i, (offset, entries) in enumerate(sorted_entries[:-1]):
			# get the offset of the next pointer, substract this offset
			data_size = sorted_entries[i + 1][0] - offset
			for entry in entries:
				entry.struct_ptr.data_size = data_size

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

	def move_empty_pointers_to_end(self):
		for offset, entries in self.offset_2_struct_entries.items():
			for entry in entries:
				if entry.struct_ptr.data_size == 0:
					if entry.struct_ptr.data_offset != self.get_size():
						logging.warning(f"Empty pointer is not at end of pool, will work but mess with the stack log")

