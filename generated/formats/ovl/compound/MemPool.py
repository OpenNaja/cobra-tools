
import logging
import io

from generated.formats.ovl_base.basic import ConvStream
from modules.formats.shared import get_padding


from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.struct import StructBase


class MemPool(StructBase):

	"""
	Description of one archive header entry
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
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

	def set_defaults(self):
		if self.context.version >= 17:
			self.zero_1 = 0
		self.size = 0
		self.offset = 0
		if self.context.version <= 15:
			self.zero_2 = 0
		self.file_hash = 0
		if self.context.version <= 15:
			self.disney_zero = 0
			self.num_files = 0
		if self.context.version >= 17:
			self.num_files = 0
		if self.context.version >= 19:
			self.ext_hash = 0
			self.zero_3 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.context.version >= 17:
			instance.zero_1 = stream.read_uint64()
		instance.size = stream.read_uint()
		instance.offset = stream.read_uint()
		if instance.context.version <= 15:
			instance.zero_2 = stream.read_uint64()
		instance.file_hash = stream.read_uint()
		if instance.context.version <= 15:
			instance.disney_zero = stream.read_ushort()
			instance.num_files = stream.read_ushort()
		if instance.context.version >= 17:
			instance.num_files = stream.read_uint()
		if instance.context.version >= 19:
			instance.ext_hash = stream.read_uint()
			instance.zero_3 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version >= 17:
			stream.write_uint64(instance.zero_1)
		stream.write_uint(instance.size)
		stream.write_uint(instance.offset)
		if instance.context.version <= 15:
			stream.write_uint64(instance.zero_2)
		stream.write_uint(instance.file_hash)
		if instance.context.version <= 15:
			stream.write_ushort(instance.disney_zero)
			stream.write_ushort(instance.num_files)
		if instance.context.version >= 17:
			stream.write_uint(instance.num_files)
		if instance.context.version >= 19:
			stream.write_uint(instance.ext_hash)
			stream.write_uint(instance.zero_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		if instance.context.version >= 17:
			yield ('zero_1', Uint64, (0, None))
		yield ('size', Uint, (0, None))
		yield ('offset', Uint, (0, None))
		if instance.context.version <= 15:
			yield ('zero_2', Uint64, (0, None))
		yield ('file_hash', Uint, (0, None))
		if instance.context.version <= 15:
			yield ('disney_zero', Ushort, (0, None))
			yield ('num_files', Ushort, (0, None))
		if instance.context.version >= 17:
			yield ('num_files', Uint, (0, None))
		if instance.context.version >= 19:
			yield ('ext_hash', Uint, (0, None))
			yield ('zero_3', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'MemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* file_hash = {fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* disney_zero = {fmt_member(self.disney_zero, indent+1)}'
		s += f'\n	* num_files = {fmt_member(self.num_files, indent+1)}'
		s += f'\n	* ext_hash = {fmt_member(self.ext_hash, indent+1)}'
		s += f'\n	* zero_3 = {fmt_member(self.zero_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

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

