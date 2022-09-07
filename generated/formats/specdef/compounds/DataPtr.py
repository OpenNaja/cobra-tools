from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DataPtr(MemStruct):

	"""
	#ARG# is dtype
	"""

	__name__ = 'DataPtr'

	_import_path = 'generated.formats.specdef.compounds.DataPtr'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data_ptr = Pointer(self.context, self.arg.dtype, DataPtr._import_path_map["generated.formats.specdef.compounds.Data"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.data_ptr = Pointer(self.context, self.arg.dtype, DataPtr._import_path_map["generated.formats.specdef.compounds.Data"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.data_ptr = Pointer.from_stream(stream, instance.context, instance.arg.dtype, DataPtr._import_path_map["generated.formats.specdef.compounds.Data"])
		if not isinstance(instance.data_ptr, int):
			instance.data_ptr.arg = instance.arg.dtype

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.data_ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data_ptr', Pointer, (instance.arg.dtype, DataPtr._import_path_map["generated.formats.specdef.compounds.Data"]), (False, None)

	def get_info_str(self, indent=0):
		return f'DataPtr [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
