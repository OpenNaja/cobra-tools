# START_GLOBALS
import io
import logging

from generated.io import BinaryStream
from modules.formats.shared import assign_versions, get_padding


# END_GLOBALS


class HeaderPointer:

# START_CLASS


	def __init__(self, context, arg=None, template=None):
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

		# generally all ptrs store data, only frag ptr 0 is just a reference
		self.is_ref_ptr = True

	# def read_data(self):
	# 	"""Load data from archive header data readers into pointer for modification and io"""
	# 	if self.pool_index == -1:
	# 		self.data = None
	# 	else:
	# 		self.data = self.read_from_pool(self.data_size)

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

	def read_from_pool(self, data_size):
		return self.pool.get_at(self.data_offset, data_size)

	def write_to_pool(self, data):
		if self.pool:
			# seek to end of pool
			self.pool.data.seek(0, 2)
			self.data_offset = self.pool.data.tell()
			self.data_size = len(data)
			self.pool.data.write(data)

	def strip_zstring_padding(self):
		"""Move surplus padding into the padding attribute"""
		# the actual zstring content + end byte
		data = self.data.split(b"\x00")[0] + b"\x00"
		# do the split itself
		self.split_data_padding(len(data))

	def split_data_padding(self, cut):
		"""Move a fixed surplus padding into the padding attribute"""
		_d = self.data_size + self.padding_size
		self.data_size = cut
		self.padding_size = _d - cut

	def link_to_pool(self, pools, is_ref_ptr=True):
		"""Link this pointer to its pool"""

		self.is_ref_ptr = is_ref_ptr
		if self.pool_index != -1:
			# get pool
			self.pool = pools[self.pool_index]
			if not is_ref_ptr:
				self.data_size = 8
			if self.data_offset not in self.pool.pointer_map:
				self.pool.pointer_map[self.data_offset] = []
			self.pool.pointer_map[self.data_offset].append(self)

	def update_pool_index(self, pools_lut):
		"""Changes self.pool_index according to self.pool in pools_lut"""

		if self.pool:
			self.pool_index = pools_lut[self.pool]
		else:
			self.pool_index = -1

	def update_data(self, data, update_copies=False, pad_to=None, include_old_pad=False):
		"""Update data and size of this pointer"""
		self._data = data

	def load_as(self, cls, num=1, version_info={}, args=()):
		"""Return self.data as codegen cls"""
		insts = []
		with BinaryStream(self.data) as stream:
			for i in range(num):
				inst = cls(self.context, *args)
				inst.read(stream)
				insts.append(inst)
		return insts

	def remove(self):
		"""Remove this pointer from suitable pool"""
		if self.pool:
			# add it to the stack
			self._data = b""

	def __eq__(self, other):
		if isinstance(other, HeaderPointer):
			return self.data_offset == other.data_offset and self.pool_index == other.pool_index

	def __repr__(self):
		return f"[{self.pool_index} | {self.data_offset}]"
