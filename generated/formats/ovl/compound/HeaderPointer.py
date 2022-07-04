
import logging
import traceback

from generated.array import Array
from generated.formats.ovl_base.basic import ConvStream


from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class HeaderPointer:

	"""
	Not standalone, used by RootEntry, Fragment and DependencyEntry
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

	@property
	def data(self):
		"""Get data from pool writer"""
		if self.pool:
			return self.pool.get_at(self.data_offset, self.data_size)

	@property
	def stream(self):
		"""Get stream from pool"""
		if self.pool:
			self.pool.data.seek(self.data_offset)
			return self.pool.data

	def write_instance(self, cls, instance):
		"""Write instance to end of stream and set offset"""
		logging.debug(f"write_instance of class {cls.__name__}")
		# align pointer
		if isinstance(instance, str):
			alignment = 1
		else:
			alignment = 16
		if self.pool:
			# seek to end of pool
			self.pool.data.seek(0, 2)
			if alignment > 1:
				offset = self.pool.data.tell()
				padding = (alignment - (offset % alignment)) % alignment
				if padding:
					self.pool.data.write(b"\x00" * padding)
					logging.debug(f"Aligned pointer from {offset} to {self.pool.data.tell()} with {padding} bytes, alignment = {alignment}")
			self.data_offset = self.pool.data.tell()
			if isinstance(instance, Array):
				Array.to_stream(self.pool.data, instance, (len(instance),), cls, instance.context, 0, None)
			else:
				cls.to_stream(self.pool.data, instance)
			self.data_size = self.pool.data.tell() - self.data_offset
			logging.debug(f"start at {self.data_offset}, size {self.data_size}")
		else:
			logging.warning(f"Pool missing, can not write {cls}")

	def write_to_pool(self, data, overwrite=False):
		if self.pool:
			if overwrite:
				# write at old data_offset
				if self.data_size != len(data):
					logging.warning(f"Data size for overwritten pointer has changed from {self.data_size} to {len(data)}!")
				self.pool.data.seek(self.data_offset)
			else:
				# seek to end of pool
				self.pool.data.seek(0, 2)
				self.data_offset = self.pool.data.tell()
			self.data_size = len(data)
			self.pool.data.write(data)

	def assign_pool(self, pools):
		"""Link this pointer to its pool"""
		if self.pool_index != -1:
			# get pool
			try:
				self.pool = pools[self.pool_index]
			except IndexError:
				raise IndexError(f"Pool index {self.pool_index} exceeds of {len(pools)} pools")

	def update_pool_index(self, pools_lut):
		"""Changes self.pool_index according to self.pool in pools_lut"""

		if self.pool:
			self.pool_index = pools_lut[self.pool]
		else:
			self.pool_index = -1

	def remove(self):
		"""Remove this pointer and all of its link children from suitable pool"""
		if self.pool:
			if self.data_offset in self.pool.offset_2_struct_entries:
				# logging.debug(f"Removed struct at offset {self.data_offset} from pool")
				structs = self.pool.offset_2_struct_entries.pop(self.data_offset)
				for entry in structs:
					for c in entry.struct_ptr.children:
						offset = c.link_ptr.data_offset
						if offset in self.pool.offset_2_link_entry:
							# logging.debug(f"Removed link at offset {offset} from pool")
							self.pool.offset_2_link_entry.pop(offset)

	def add_struct(self, entry):
		"""Adds an entry to the required tables of this pool"""
		if self.pool:
			if self.data_offset not in self.pool.offset_2_struct_entries:
				self.pool.offset_2_struct_entries[self.data_offset] = []
			self.pool.offset_2_struct_entries[self.data_offset].append(entry)

	def add_link(self, entry):
		"""Adds an entry to the required tables of this pool"""
		if self.pool:
			self.pool.offset_2_link_entry[self.data_offset] = entry
			self.data_size = 8

	def del_struct(self):
		"""Adds an entry to the required tables of this pool"""
		if self.pool:
			if self.data_offset in self.pool.offset_2_struct_entries:
				self.pool.offset_2_struct_entries.pop(self.data_offset)

	def del_link(self):
		if self.pool:
			if self.data_offset in self.pool.offset_2_link_entry:
				self.pool.offset_2_link_entry.pop(self.data_offset)

	def replace_bytes(self, byte_name_tups):
		"""Replaces the bytes tuples in byte_name_tups"""
		b = self.data
		for old, new in byte_name_tups:
			b = b.replace(old, new)
		self.write_to_pool(b, overwrite=True)

	def __eq__(self, other):
		if isinstance(other, HeaderPointer):
			return self.data_offset == other.data_offset and self.pool_index == other.pool_index

	def __repr__(self):
		return f"[{self.pool_index: 3} | {self.data_offset: 6}]"

	def __hash__(self):
		return hash((self.pool_index, self.data_offset))

