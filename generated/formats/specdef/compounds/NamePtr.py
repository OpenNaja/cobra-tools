from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class NamePtr(MemStruct):

	__name__ = 'NamePtr'

	_import_path = 'generated.formats.specdef.compounds.NamePtr'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.name_ptr = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.name_ptr = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.name_ptr = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.name_ptr, int):
			instance.name_ptr.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.name_ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'name_ptr', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'NamePtr [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
