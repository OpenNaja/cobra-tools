from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DataStreamResourceDataList(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'DataStreamResourceDataList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data_stream_resource_data_count = name_type_map['Uint64'](self.context, 0, None)
		self.data_stream_resource_data = name_type_map['ArrayPointer'](self.context, self.data_stream_resource_data_count, name_type_map['DataStreamResourceData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data_stream_resource_data_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data_stream_resource_data', name_type_map['ArrayPointer'], (None, name_type_map['DataStreamResourceData']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data_stream_resource_data_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data_stream_resource_data', name_type_map['ArrayPointer'], (instance.data_stream_resource_data_count, name_type_map['DataStreamResourceData']), (False, None)
