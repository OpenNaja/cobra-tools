
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
		new_ss = SizedStringEntry()
		self.ovs.transfer_identity(new_ss, file_entry)
		new_pointss = HeaderPointer()
		new_ss.pointers.append(new_pointss)
		self.ovs.sized_str_entries.append(new_ss)
		return new_ss

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
#
#
# if file_entry.ext == ".fdb":
# 	self.pool_data += struct.pack("I28s", len(dbuffer), b'')
# 	new_ss = self.create_ss_entry(file_entry)
# 	new_ss.pointers[0].pool_index = 0
# 	new_ss.pointers[0].data_offset = offset
# 	new_data = self.create_data_entry(file_entry, (file_name_bytes, dbuffer))
# 	new_data.set_index = 0
#
# if file_entry.ext == ".userinterfaceicondata":  # userinterfaceicondata, 2 frags
# 	icname, icpath = [line.strip() for line in dbuffer.split(b'\n') if line.strip()]
# 	outb = zstr(icname) + zstr(icpath)
# 	outb = outb + get_padding(len(outb), 64) + struct.pack('8s', b'')
# 	self.pool_data += outb
# 	newoffset = len(self.pool_data)
# 	self.pool_data += struct.pack('16s', b'')
# 	new_frag0 = self.create_fragment()
# 	new_frag0.pointers[0].pool_index = 0
# 	new_frag0.pointers[0].data_offset = newoffset
# 	new_frag0.pointers[1].pool_index = 0
# 	new_frag0.pointers[1].data_offset = offset
# 	new_frag1 = self.create_fragment()
# 	new_frag1.pointers[0].pool_index = 0
# 	new_frag1.pointers[0].data_offset = newoffset + 8
# 	new_frag1.pointers[1].pool_index = 0
# 	new_frag1.pointers[1].data_offset = offset + len(icname) + 1
# 	new_ss = self.create_ss_entry(file_entry)
# 	new_ss.pointers[0].pool_index = 0
# 	new_ss.pointers[0].data_offset = newoffset
#
# if file_entry.ext == ".txt":
# 	data = struct.pack("I", len(dbuffer)) + zstr(dbuffer)
# 	self.pool_data += data + get_padding(len(data), alignment=8)  # fragment pointer 1 data
# 	new_ss = self.create_ss_entry(file_entry)
# 	new_ss.pointers[0].pool_index = 0
# 	new_ss.pointers[0].data_offset = offset
# 	file_entry_count += 1
