# START_GLOBALS
import io
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
		self.padding = b""

	def read_data(self):
		"""Load data from archive header data readers into pointer for modification and io"""
		if self.pool_index == -1:
			self.data = None
		else:
			self.pool.data.seek(self.data_offset)
			self.data = self.pool.data.read(self.data_size)

	def write_data(self, update_copies=False):
		"""Write data to header data, update offset, also for copies if told"""

		if self.pool_index != -1:
			# update data offset
			self.data_offset = self.pool.data.tell()
			if update_copies:
				for other_pointer in self.copies:
					other_pointer.data_offset = self.pool.data.tell()
			# write data to io, adjusting the cursor for that header
			self.pool.data.write(self.data + self.padding)

	def strip_zstring_padding(self):
		"""Move surplus padding into the padding attribute"""
		# the actual zstring content + end byte
		data = self.data.split(b"\x00")[0] + b"\x00"
		# do the split itself
		self.split_data_padding(len(data))

	def split_data_padding(self, cut):
		"""Move a fixed surplus padding into the padding attribute"""
		_d = self.data + self.padding
		self.padding = _d[cut:]
		self.data = _d[:cut]

	def link_to_pool(self, pools):
		"""Link this pointer to its pool"""

		if self.pool_index != -1:
			# get pool
			self.pool = pools[self.pool_index]
			if self.data_offset not in self.pool.pointer_map:
				self.pool.pointer_map[self.data_offset] = []
			self.pool.pointer_map[self.data_offset].append(self)

	def update_data(self, data, update_copies=False, pad_to=None, include_old_pad=False):
		"""Update data and size of this pointer"""
		self.data = data
		# only change padding if a new alignment is given
		if pad_to:
			len_d = len(data)
			# consider the old padding for alignment?
			if include_old_pad:
				len_d += len(self.padding)
			new_pad = get_padding(len_d, pad_to)
			# append new to the old padding
			if include_old_pad:
				self.padding = self.padding + new_pad
			# overwrite the old padding
			else:
				self.padding = new_pad
		self.data_size = len(self.data + self.padding)
		# update other pointers if asked to by the injector
		if update_copies and self.pool_index != -1:
			for other_pointer in self.copies:
				if other_pointer is not self:
					other_pointer.update_data(data, pad_to=pad_to, include_old_pad=include_old_pad)

	def load_as(self, cls, num=1, version_info={}, args=()):
		"""Return self.data as codegen cls
		version_info must be a dict that has version & user_version attributes"""
		with BinaryStream(self.data) as stream:
			assign_versions(stream, version_info)
			insts = []
			for i in range(num):
				inst = cls(*args)
				inst.read(stream)
				insts.append(inst)
		return insts

	def remove(self, archive):
		"""Remove this pointer from suitable header entry"""

		if self.pool_index == -1:
			pass
		else:
			# get header entry
			entry = archive.pools[self.pool_index]
			if self.data_offset in entry.pointer_map:
				entry.pointer_map.pop(self.data_offset)

