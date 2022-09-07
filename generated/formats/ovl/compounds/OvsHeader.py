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

	__name__ = 'OvsHeader'

	_import_path = 'generated.formats.ovl.compounds.OvsHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pool_groups = Array(self.context, 0, None, (0,), PoolGroup)
		self.pools = Array(self.context, 0, None, (0,), MemPool)
		self.data_entries = Array(self.context, 0, None, (0,), DataEntry)
		self.buffer_entries = Array(self.context, 0, None, (0,), BufferEntry)
		self.buffer_groups = Array(self.context, 0, None, (0,), BufferGroup)
		self.root_entries = Array(self.context, 0, None, (0,), RootEntry)
		self.fragments = Array(self.context, 0, None, (0,), Fragment)
		self.set_header = SetHeader(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.pool_groups = Array(self.context, 0, None, (self.arg.num_pool_groups,), PoolGroup)
		self.pools = Array(self.context, 0, None, (self.arg.num_pools,), MemPool)
		self.data_entries = Array(self.context, 0, None, (self.arg.num_datas,), DataEntry)
		self.buffer_entries = Array(self.context, 0, None, (self.arg.num_buffers,), BufferEntry)
		self.buffer_groups = Array(self.context, 0, None, (self.arg.num_buffer_groups,), BufferGroup)
		self.root_entries = Array(self.context, 0, None, (self.arg.num_root_entries,), RootEntry)
		self.fragments = Array(self.context, 0, None, (self.arg.num_fragments,), Fragment)
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
		Array.to_stream(stream, instance.pool_groups, instance.context, 0, None, (instance.arg.num_pool_groups,), PoolGroup)
		Array.to_stream(stream, instance.pools, instance.context, 0, None, (instance.arg.num_pools,), MemPool)
		Array.to_stream(stream, instance.data_entries, instance.context, 0, None, (instance.arg.num_datas,), DataEntry)
		Array.to_stream(stream, instance.buffer_entries, instance.context, 0, None, (instance.arg.num_buffers,), BufferEntry)
		Array.to_stream(stream, instance.buffer_groups, instance.context, 0, None, (instance.arg.num_buffer_groups,), BufferGroup)
		Array.to_stream(stream, instance.root_entries, instance.context, 0, None, (instance.arg.num_root_entries,), RootEntry)
		Array.to_stream(stream, instance.fragments, instance.context, 0, None, (instance.arg.num_fragments,), Fragment)
		SetHeader.to_stream(stream, instance.set_header)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pool_groups', Array, (0, None, (instance.arg.num_pool_groups,), PoolGroup), (False, None)
		yield 'pools', Array, (0, None, (instance.arg.num_pools,), MemPool), (False, None)
		yield 'data_entries', Array, (0, None, (instance.arg.num_datas,), DataEntry), (False, None)
		yield 'buffer_entries', Array, (0, None, (instance.arg.num_buffers,), BufferEntry), (False, None)
		yield 'buffer_groups', Array, (0, None, (instance.arg.num_buffer_groups,), BufferGroup), (False, None)
		yield 'root_entries', Array, (0, None, (instance.arg.num_root_entries,), RootEntry), (False, None)
		yield 'fragments', Array, (0, None, (instance.arg.num_fragments,), Fragment), (False, None)
		yield 'set_header', SetHeader, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'OvsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
