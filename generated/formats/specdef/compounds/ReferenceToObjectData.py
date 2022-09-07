from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ReferenceToObjectData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = 'ReferenceToObjectData'

	_import_path = 'generated.formats.specdef.compounds.ReferenceToObjectData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ioptional = 0
		self.obj_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ioptional = 0
		self.obj_name = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.obj_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.ioptional = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.obj_name, int):
			instance.obj_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.obj_name)
		Uint.to_stream(stream, instance.ioptional)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'obj_name', Pointer, (0, ZString), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ReferenceToObjectData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
