# START_GLOBALS
import logging
import numpy as np
from generated.array import Array
from generated.base_struct import BaseStruct


# END_GLOBALS


class HeaderPointer(BaseStruct):

# START_CLASS

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		# The index of the MemPool this one relates to; OR, for entries referred to from AssetEntries: -1 (FF FF FF FF)
		self.pool_index = 0

		# the byte offset relative to the start of the header entry data
		self.data_offset = 0

		# define this already
		self.pool = None
		self.data_size = 0
		if set_default:
			self.set_defaults()

	@property
	def data(self):
		"""Get data from pool writer"""
		if self.pool:
			return self.pool.get_at(self.data_offset, self.data_size)

	@classmethod
	def get_stream(cls, instance, pools):
		"""Get stream from pool"""
		pool = cls.get_pool(instance, pools)
		if pool:
			pool.data.seek(instance.data_offset)
			return pool.data

	@property
	def stream(self):
		"""Get stream from pool"""
		if self.pool:
			self.pool.data.seek(self.data_offset)
			return self.pool.data

	def align_write(self, data, overwrite=False):
		"""Prepares self.pool.data for writing, handling alignment according to type of data"""
		if self.pool:
			if overwrite:
				# write at old data_offset, but then check for size match
				if isinstance(data, (bytes, bytearray, str)) and self.data_size != len(data):
					logging.warning(f"Data size for overwritten pointer has changed from {self.data_size} to {len(data)}!")
				self.pool.data.seek(self.data_offset)
			else:
				# seek to end of pool
				self.pool.data.seek(0, 2)
				# check for alignment
				if isinstance(data, str):
					alignment = 1
				else:
					alignment = 16
				# logging.info(f"{type(data)} {data} alignment {alignment}")
				# write alignment to pool
				if alignment > 1:
					offset = self.pool.data.tell()
					padding = (alignment - (offset % alignment)) % alignment
					if padding:
						self.pool.data.write(b"\x00" * padding)
						logging.debug(
							f"Aligned pointer from {offset} to {self.pool.data.tell()} with {padding} bytes, alignment = {alignment}")
				self.data_offset = self.pool.data.tell()
			return True

	def write_instance(self, cls, instance):
		"""Write instance to end of stream and set offset"""
		context = None
		# logging.info(f"write_instance {cls} {instance}")
		if self.align_write(instance, overwrite=False):
			if instance is None:
				logging.info(f"Can't write None for clas {cls}")
			elif isinstance(instance, (Array, np.ndarray)):
				Array.to_stream(instance, self.pool.data, context, dtype=cls)
			else:
				cls.to_stream(instance, self.pool.data, context)
			self.data_size = self.pool.data.tell() - self.data_offset
			logging.debug(f"start at {self.data_offset}, size {self.data_size}")
		else:
			logging.warning(f"Pool missing, can not write {cls}")

	def write_to_pool(self, data, overwrite=False):
		# logging.info(f"write_to_pool overwrite={overwrite}")
		if self.align_write(data, overwrite=overwrite):
			self.data_size = len(data)
			self.pool.data.write(data)
		logging.debug(f"write_to_pool size {self.data_size}")

	@classmethod
	def get_pool(cls, instance, pools):
		if instance.pool_index != -1:
			return pools[instance.pool_index]

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
	@classmethod
	def add_struct(cls, instance, entry, pools):
		"""Adds an entry to the required tables of this pool"""
		pool = cls.get_pool(instance, pools)
		if pool:
			if instance.data_offset not in pool.offset_2_struct_entries:
				pool.offset_2_struct_entries[instance.data_offset] = []
			pool.offset_2_struct_entries[instance.data_offset].append(entry)

	@classmethod
	def add_link(cls, instance, entry, pools):
		"""Adds an entry to the required tables of this pool"""
		pool = cls.get_pool(instance, pools)
		if pool:
			pool.offset_2_link_entry[instance.data_offset] = entry
			# self.data_size = 8

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
