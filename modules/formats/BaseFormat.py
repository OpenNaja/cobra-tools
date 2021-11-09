
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.MemPool import MemPool
from generated.formats.ovl.compound.PoolType import PoolType
from generated.formats.ovl.compound.SizedStringEntry import SizedStringEntry
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.io import BinaryStream


class BaseFile:

	def __init__(self, ovl):
		self.ovl = ovl
		self.ovs = ovl.static_archive.content

	def assign_ss_entry(self, file_entry):
		self.sized_str_entry = self.ovl.get_sized_str_entry(file_entry.name)

	def assign_fixed_frags(self, ovl, file_entry, count):
		self.assign_ss_entry(file_entry)
		ss_pointer = self.sized_str_entry.pointers[0]
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, count)

	def get_pool(self, pool_type_key):
		# get one if it exists
		for pool_index, pool in enumerate(self.ovs.pools):
			if pool.type == pool_type_key:
				return pool_index, pool
		# nope, means we gotta create pool type and pool
		pool_type = PoolType(self.ovl.context)
		pool_type.type = pool_type_key
		pool_type.num_pools = 1

		pool = MemPool(self.ovl.context)
		pool.data = BinaryStream()
		# the real address isn't known until it is written, but declare it anyway
		pool.address = 0
		# assign_versions(pool.data, get_versions(self.ovl))
		pool.type = pool_type_key
		self.ovs.pool_types.append(pool_type)
		self.ovs.pools.append(pool)
		return len(self.ovs.pools)-1, pool

	def create(self, ovs, file_entry):
		raise NotImplementedError

	def get_content(self, filename):
		with open(filename, 'rb') as f:
			content = f.read()
		return content

	def get_file_entry(self, file_name):
		for file_entry in self.ovl.files:
			if file_entry.name == file_name:
				return file_entry

	def create_ss_entry(self, file_entry):
		ss_entry = SizedStringEntry(self.ovl.context)
		ss_entry.children = []
		ss_entry.fragments = []
		self.ovs.transfer_identity(ss_entry, file_entry)
		new_pointss = HeaderPointer(self.ovl.context)
		ss_entry.pointers.append(new_pointss)
		self.ovs.sized_str_entries.append(ss_entry)
		return ss_entry

	def create_fragment(self):
		new_frag = Fragment(self.ovl.context)
		new_point0 = HeaderPointer(self.ovl.context)
		new_point1 = HeaderPointer(self.ovl.context)
		new_frag.pointers.append(new_point0)
		new_frag.pointers.append(new_point1)
		self.ovs.fragments.append(new_frag)
		return new_frag

	def create_data_entry(self, ss_entry, buffer_bytes):
		new_data = DataEntry(self.ovl.context)
		self.ovs.transfer_identity(new_data, ss_entry)
		ss_entry.data_entry = new_data
		new_data.buffer_count = len(buffer_bytes)
		new_data.buffers = []
		for i, b in enumerate(buffer_bytes):
			new_buff = BufferEntry(self.ovl.context)
			self.ovs.transfer_identity(new_buff, ss_entry)
			new_buff.index = i
			new_data.buffers.append(new_buff)
			self.ovs.buffer_entries.append(new_buff)
		self.ovs.data_entries.append(new_data)
		new_data.update_data(buffer_bytes)
		return new_data

	def update(self):
		"""Don't do anything by default, overwrite if needed"""
		pass
