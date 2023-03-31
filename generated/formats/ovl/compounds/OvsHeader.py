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

	_import_key = 'ovl.compounds.OvsHeader'

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

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('pool_groups', Array, (0, None, (None,), PoolGroup), (False, None), None)
		yield ('pools', Array, (0, None, (None,), MemPool), (False, None), None)
		yield ('data_entries', Array, (0, None, (None,), DataEntry), (False, None), None)
		yield ('buffer_entries', Array, (0, None, (None,), BufferEntry), (False, None), None)
		yield ('buffer_groups', Array, (0, None, (None,), BufferGroup), (False, None), None)
		yield ('root_entries', Array, (0, None, (None,), RootEntry), (False, None), None)
		yield ('fragments', Array, (0, None, (None,), Fragment), (False, None), None)
		yield ('set_header', SetHeader, (0, None), (False, None), None)

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


OvsHeader.init_attributes()
