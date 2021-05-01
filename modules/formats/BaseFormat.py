
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.HeaderEntry import MemPool
from generated.formats.ovl.compound.HeaderType import PoolType
from generated.formats.ovl.compound.SizedStringEntry import SizedStringEntry
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.io import BinaryStream


class BaseFile:
	# dbuffer = self.getContent(file_entry.path)
	# file_name_bytes = bytearray(file_entry.basename, encoding='utf8')

	def assign_fixed_frags(self, ovl, file_entry, count):
		self.ovl = ovl
		self.ovs = ovl.static_archive.content
		self.sized_str_entry = self.ovl.ss_dict[file_entry.name]
		ss_pointer = self.sized_str_entry.pointers[0]
		frags = self.ovs.pools[ss_pointer.pool_index].fragments
		self.sized_str_entry.fragments = self.ovs.get_frags_after_count(frags, ss_pointer.address, count)

	def get_pool(self, pool_type):
		# get one if it exists
		for pool_index, pool in enumerate(self.ovs.pools):
			if pool.type == pool_type:
				return pool_index, pool
		# nope, means we gotta create pool type and pool
		header_type = PoolType()
		header_type.type = pool_type
		header_type.num_pools = 1

		pool = MemPool()
		# pool.data = io.BytesIO(self.pool_data)
		# pool.size = len(self.pool_data)
		pool.data = BinaryStream()
		# assign_versions(pool.data, get_versions(self.ovl))
		pool.type = type
		# pool.offset = 0
		# pool.num_files = file_entry_count
		pool.type = header_type.type
		self.ovs.pool_types.append(header_type)
		self.ovs.pools.append(pool)
		return len(self.ovs.pools)-1, pool

	def create(self, ovs, fp):
		raise NotImplementedError

	def getContent(self, filename):
		with open(filename, 'rb') as f:
			content = f.read()
		return content

	def create_ss_entry(self, file_entry):
		ss_entry = SizedStringEntry()
		ss_entry.children = []
		self.ovs.transfer_identity(ss_entry, file_entry)
		new_pointss = HeaderPointer()
		ss_entry.pointers.append(new_pointss)
		self.ovs.sized_str_entries.append(ss_entry)
		return ss_entry

	def create_fragment(self):
		new_frag = Fragment()
		new_point0 = HeaderPointer()
		new_point1 = HeaderPointer()
		new_frag.pointers.append(new_point0)
		new_frag.pointers.append(new_point1)
		self.ovs.fragments.append(new_frag)
		return new_frag

	def create_data_entry(self, file_entry, buffer_bytes):
		new_data = DataEntry()
		self.ovs.transfer_identity(new_data, file_entry)
		# new_data.set_index = 0
		new_data.buffer_count = len(buffer_bytes)
		new_data.size_1 = sum([len(b) for b in buffer_bytes])
		for i, b in reversed(list(enumerate(buffer_bytes))):
			new_buff = BufferEntry()
			new_buff.index = i
			new_buff.update_data(b)
			self.ovs.buffer_entries.append(new_buff)
		self.ovs.data_entries.append(new_data)
		return new_data
