from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ZStrPtr(MemStruct):

	"""
	need to wrap this to avoid setting arg on the np arrarys
	"""

	__name__ = 'ZStrPtr'

	_import_path = 'generated.formats.renderparameters.compounds.ZStrPtr'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.string = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.string = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.string = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.string, int):
			instance.string.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.string)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'string', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'ZStrPtr [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
