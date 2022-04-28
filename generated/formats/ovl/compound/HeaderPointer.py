
import logging
import traceback

from generated.array import Array
from generated.formats.ovl_base.basic import ConvStream


from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class HeaderPointer:

	"""
	Not standalone, used by SizedStringEntry, Fragment and DependencyEntry
	"""

	context = ContextReference()

	def set_defaults(self):
		self.pool_index = 0
		self.data_offset = 0

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
		instance.pool_index = stream.read_int()
		instance.data_offset = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_int(instance.pool_index)
		stream.write_uint(instance.data_offset)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# The index of the MemPool this one relates to; OR, for entries referred to from AssetEntries: -1 (FF FF FF FF)
		self.pool_index = 0

		# the byte offset relative to the start of the header entry data
		self.data_offset = 0

		# define this already
		self.pool = None
		self.data_size = 0
		self.padding_size = 0

		# temp data for flushing
		self._data = None

		# sizedstr and frag ptr 1 point to structs, whereas frag ptr 0 and dependency are just a reference
		self.is_struct_ptr = True

	@property
	def data(self, with_padding=False):
		"""Get data from pool writer"""
		if self.pool:
			s = self.data_size
			if with_padding:
				s += self.padding_size
			return self.read_from_pool(s)

	@property
	def padding(self):
		"""Get padding from pool writer"""
		if self.pool:
			return self.pool.get_at(self.data_offset+self.data_size, self.padding_size)

	@property
	def stream(self):
		"""Get stream from pool"""
		if self.pool:
			self.pool.data.seek(self.data_offset)
			return self.pool.data

	def write_instance(self, cls, instance):
		"""Write instance to end of stream and set offset"""
		logging.debug(f"write_instance of class {cls}")
		if self.pool:
			# seek to end of pool
			self.pool.data.seek(0, 2)
			self.data_offset = self.pool.data.tell()
			if isinstance(instance, Array):
				Array.to_stream(self.pool.data, instance, (len(instance),), cls, instance.context, 0, None)
			else:
				cls.to_stream(self.pool.data, instance)
			self.data_size = self.pool.data.tell() - self.data_offset
			logging.debug(f"start at {self.data_offset}, size {self.data_size}")
		else:
			logging.warning(f"Pool missing, can not write {cls}")

	def read_from_pool(self, data_size):
		return self.pool.get_at(self.data_offset, data_size)

	def write_to_pool(self, data):
		if self.pool:
			# seek to end of pool
			self.pool.data.seek(0, 2)
			self.data_offset = self.pool.data.tell()
			self.data_size = len(data)
			self.pool.data.write(data)

	def link_to_pool(self, pools, is_struct_ptr=True):
		"""Link this pointer to its pool"""

		self.is_struct_ptr = is_struct_ptr
		if self.pool_index != -1:
			# get pool
			self.pool = pools[self.pool_index]
			if not is_struct_ptr:
				self.data_size = 8
			# else:
			# 	# todo - only add struct ptrs to map, but ensure that non-struct ptrs have their offsets adjusted for delete
			# 	if self.data_offset not in self.pool.offset_2_struct_entries:
			# 		self.pool.offset_2_struct_entries[self.data_offset] = []
			# 	self.pool.offset_2_struct_entries[self.data_offset].append(self)

	def update_pool_index(self, pools_lut):
		"""Changes self.pool_index according to self.pool in pools_lut"""

		if self.pool:
			self.pool_index = pools_lut[self.pool]
		else:
			self.pool_index = -1

	def update_data(self, data, update_copies=False, pad_to=None, include_old_pad=False):
		"""Update data and size of this pointer"""
		assert self.is_struct_ptr
		self._data = data

	def remove(self):
		"""Remove this pointer from suitable pool"""
		if self.pool:
			# add it to the stack
			self._data = b""

	def __eq__(self, other):
		if isinstance(other, HeaderPointer):
			return self.data_offset == other.data_offset and self.pool_index == other.pool_index

	def __repr__(self):
		return f"[{self.pool_index: 3} | {self.data_offset: 6}]"

	def __hash__(self):
		return hash((self.pool_index, self.data_offset))

