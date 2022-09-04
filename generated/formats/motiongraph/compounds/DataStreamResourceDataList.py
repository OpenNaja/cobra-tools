from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DataStreamResourceDataList(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'DataStreamResourceDataList'

	_import_path = 'generated.formats.motiongraph.compounds.DataStreamResourceDataList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.data_stream_resource_data = Pointer(self.context, self.count, DataStreamResourceDataList._import_path_map["generated.formats.motiongraph.compounds.DataStreamResourceDataPoints"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.data_stream_resource_data = Pointer(self.context, self.count, DataStreamResourceDataList._import_path_map["generated.formats.motiongraph.compounds.DataStreamResourceDataPoints"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data_stream_resource_data = Pointer.from_stream(stream, instance.context, instance.count, DataStreamResourceDataList._import_path_map["generated.formats.motiongraph.compounds.DataStreamResourceDataPoints"])
		if not isinstance(instance.data_stream_resource_data, int):
			instance.data_stream_resource_data.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.count)
		Pointer.to_stream(stream, instance.data_stream_resource_data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'data_stream_resource_data', Pointer, (instance.count, DataStreamResourceDataList._import_path_map["generated.formats.motiongraph.compounds.DataStreamResourceDataPoints"]), (False, None)

	def get_info_str(self, indent=0):
		return f'DataStreamResourceDataList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
