from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DataStreamResourceDataList(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'DataStreamResourceDataList'

	_import_key = 'motiongraph.compounds.DataStreamResourceDataList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.data_stream_resource_data = Pointer(self.context, self.count, DataStreamResourceDataList._import_map["motiongraph.compounds.DataStreamResourceDataPoints"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('count', Uint64, (0, None), (False, None), None),
		('data_stream_resource_data', Pointer, (None, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'data_stream_resource_data', Pointer, (instance.count, DataStreamResourceDataList._import_map["motiongraph.compounds.DataStreamResourceDataPoints"]), (False, None)
