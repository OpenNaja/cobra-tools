from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ovl.compounds.BufferEntry import BufferEntry
from generated.formats.ovl.compounds.BufferGroup import BufferGroup
from generated.formats.ovl.compounds.DataEntry import DataEntry
from generated.formats.ovl.compounds.Fragment import Fragment
from generated.formats.ovl.compounds.MemPool import MemPool
from generated.formats.ovl.compounds.PoolGroup import PoolGroup
from generated.formats.ovl.compounds.RootEntry import RootEntry
from generated.formats.ovl.compounds.SetHeader import SetHeader


class OvsHeader(BaseStruct):

	"""
	Description of one archive's content
	"""

	__name__ = OvsHeader

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pool_groups = Array((0,), PoolGroup, self.context, 0, None)
		self.pools = Array((0,), MemPool, self.context, 0, None)
		self.data_entries = Array((0,), DataEntry, self.context, 0, None)
		self.buffer_entries = Array((0,), BufferEntry, self.context, 0, None)
		self.buffer_groups = Array((0,), BufferGroup, self.context, 0, None)
		self.root_entries = Array((0,), RootEntry, self.context, 0, None)
		self.fragments = Array((0,), Fragment, self.context, 0, None)
		self.set_header = SetHeader(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.pool_groups = Array((self.arg.num_pool_groups,), PoolGroup, self.context, 0, None)
		self.pools = Array((self.arg.num_pools,), MemPool, self.context, 0, None)
		self.data_entries = Array((self.arg.num_datas,), DataEntry, self.context, 0, None)
		self.buffer_entries = Array((self.arg.num_buffers,), BufferEntry, self.context, 0, None)
		self.buffer_groups = Array((self.arg.num_buffer_groups,), BufferGroup, self.context, 0, None)
		self.root_entries = Array((self.arg.num_root_entries,), RootEntry, self.context, 0, None)
		self.fragments = Array((self.arg.num_fragments,), Fragment, self.context, 0, None)
		self.set_header = SetHeader(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.pool_groups = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_pool_groups,), PoolGroup)
		instance.pools = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_pools,), MemPool)
		instance.data_entries = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_datas,), DataEntry)
		instance.buffer_entries = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_buffers,), BufferEntry)
		instance.buffer_groups = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_buffer_groups,), BufferGroup)
		instance.root_entries = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_root_entries,), RootEntry)
		instance.fragments = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_fragments,), Fragment)
		instance.set_header = SetHeader.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.pool_groups, (instance.arg.num_pool_groups,), PoolGroup, instance.context, 0, None)
		Array.to_stream(stream, instance.pools, (instance.arg.num_pools,), MemPool, instance.context, 0, None)
		Array.to_stream(stream, instance.data_entries, (instance.arg.num_datas,), DataEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.buffer_entries, (instance.arg.num_buffers,), BufferEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.buffer_groups, (instance.arg.num_buffer_groups,), BufferGroup, instance.context, 0, None)
		Array.to_stream(stream, instance.root_entries, (instance.arg.num_root_entries,), RootEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.fragments, (instance.arg.num_fragments,), Fragment, instance.context, 0, None)
		SetHeader.to_stream(stream, instance.set_header)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'pool_groups', Array, ((instance.arg.num_pool_groups,), PoolGroup, 0, None), (False, None)
		yield 'pools', Array, ((instance.arg.num_pools,), MemPool, 0, None), (False, None)
		yield 'data_entries', Array, ((instance.arg.num_datas,), DataEntry, 0, None), (False, None)
		yield 'buffer_entries', Array, ((instance.arg.num_buffers,), BufferEntry, 0, None), (False, None)
		yield 'buffer_groups', Array, ((instance.arg.num_buffer_groups,), BufferGroup, 0, None), (False, None)
		yield 'root_entries', Array, ((instance.arg.num_root_entries,), RootEntry, 0, None), (False, None)
		yield 'fragments', Array, ((instance.arg.num_fragments,), Fragment, 0, None), (False, None)
		yield 'set_header', SetHeader, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'OvsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* pool_groups = {self.fmt_member(self.pool_groups, indent+1)}'
		s += f'\n	* pools = {self.fmt_member(self.pools, indent+1)}'
		s += f'\n	* data_entries = {self.fmt_member(self.data_entries, indent+1)}'
		s += f'\n	* buffer_entries = {self.fmt_member(self.buffer_entries, indent+1)}'
		s += f'\n	* buffer_groups = {self.fmt_member(self.buffer_groups, indent+1)}'
		s += f'\n	* root_entries = {self.fmt_member(self.root_entries, indent+1)}'
		s += f'\n	* fragments = {self.fmt_member(self.fragments, indent+1)}'
		s += f'\n	* set_header = {self.fmt_member(self.set_header, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
