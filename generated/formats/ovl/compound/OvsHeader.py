from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.BufferGroup import BufferGroup
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.MemPool import MemPool
from generated.formats.ovl.compound.PoolGroup import PoolGroup
from generated.formats.ovl.compound.SetHeader import SetHeader
from generated.formats.ovl.compound.SizedStringEntry import SizedStringEntry


class OvsHeader:

	"""
	Description of one archive's content
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.pool_groups = Array((self.arg.num_pool_groups,), PoolGroup, self.context, 0, None)
		self.pools = Array((self.arg.num_pools,), MemPool, self.context, 0, None)
		self.data_entries = Array((self.arg.num_datas,), DataEntry, self.context, 0, None)
		self.buffer_entries = Array((self.arg.num_buffers,), BufferEntry, self.context, 0, None)
		self.buffer_groups = Array((self.arg.num_buffer_groups,), BufferGroup, self.context, 0, None)
		self.sized_str_entries = Array((self.arg.num_files,), SizedStringEntry, self.context, 0, None)
		self.fragments = Array((self.arg.num_fragments,), Fragment, self.context, 0, None)
		self.set_header = SetHeader(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.pool_groups = Array((self.arg.num_pool_groups,), PoolGroup, self.context, 0, None)
		self.pools = Array((self.arg.num_pools,), MemPool, self.context, 0, None)
		self.data_entries = Array((self.arg.num_datas,), DataEntry, self.context, 0, None)
		self.buffer_entries = Array((self.arg.num_buffers,), BufferEntry, self.context, 0, None)
		self.buffer_groups = Array((self.arg.num_buffer_groups,), BufferGroup, self.context, 0, None)
		self.sized_str_entries = Array((self.arg.num_files,), SizedStringEntry, self.context, 0, None)
		self.fragments = Array((self.arg.num_fragments,), Fragment, self.context, 0, None)
		self.set_header = SetHeader(self.context, 0, None)

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
		instance.pool_groups = Array.from_stream(stream, (instance.arg.num_pool_groups,), PoolGroup, instance.context, 0, None)
		instance.pools = Array.from_stream(stream, (instance.arg.num_pools,), MemPool, instance.context, 0, None)
		instance.data_entries = Array.from_stream(stream, (instance.arg.num_datas,), DataEntry, instance.context, 0, None)
		instance.buffer_entries = Array.from_stream(stream, (instance.arg.num_buffers,), BufferEntry, instance.context, 0, None)
		instance.buffer_groups = Array.from_stream(stream, (instance.arg.num_buffer_groups,), BufferGroup, instance.context, 0, None)
		instance.sized_str_entries = Array.from_stream(stream, (instance.arg.num_files,), SizedStringEntry, instance.context, 0, None)
		instance.fragments = Array.from_stream(stream, (instance.arg.num_fragments,), Fragment, instance.context, 0, None)
		instance.set_header = SetHeader.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		Array.to_stream(stream, instance.pool_groups, (instance.arg.num_pool_groups,), PoolGroup, instance.context, 0, None)
		Array.to_stream(stream, instance.pools, (instance.arg.num_pools,), MemPool, instance.context, 0, None)
		Array.to_stream(stream, instance.data_entries, (instance.arg.num_datas,), DataEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.buffer_entries, (instance.arg.num_buffers,), BufferEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.buffer_groups, (instance.arg.num_buffer_groups,), BufferGroup, instance.context, 0, None)
		Array.to_stream(stream, instance.sized_str_entries, (instance.arg.num_files,), SizedStringEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.fragments, (instance.arg.num_fragments,), Fragment, instance.context, 0, None)
		SetHeader.to_stream(stream, instance.set_header)

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

	def get_info_str(self):
		return f'OvsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* pool_groups = {self.pool_groups.__repr__()}'
		s += f'\n	* pools = {self.pools.__repr__()}'
		s += f'\n	* data_entries = {self.data_entries.__repr__()}'
		s += f'\n	* buffer_entries = {self.buffer_entries.__repr__()}'
		s += f'\n	* buffer_groups = {self.buffer_groups.__repr__()}'
		s += f'\n	* sized_str_entries = {self.sized_str_entries.__repr__()}'
		s += f'\n	* fragments = {self.fragments.__repr__()}'
		s += f'\n	* set_header = {self.set_header.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
