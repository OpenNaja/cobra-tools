from generated.formats.base.basic import Int64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Int64Data(MemStruct):

	"""
	48 bytes in log
	"""

	__name__ = 'Int64Data'

	_import_path = 'generated.formats.specdef.compounds.Int64Data'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		self.enum = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		self.enum = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.imin = Int64.from_stream(stream, instance.context, 0, None)
		instance.imax = Int64.from_stream(stream, instance.context, 0, None)
		instance.ivalue = Int64.from_stream(stream, instance.context, 0, None)
		instance.ioptional = Int64.from_stream(stream, instance.context, 0, None)
		instance.enum = Pointer.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.enum, int):
			instance.enum.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Int64.to_stream(stream, instance.imin)
		Int64.to_stream(stream, instance.imax)
		Int64.to_stream(stream, instance.ivalue)
		Int64.to_stream(stream, instance.ioptional)
		Pointer.to_stream(stream, instance.enum)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'imin', Int64, (0, None), (False, None)
		yield 'imax', Int64, (0, None), (False, None)
		yield 'ivalue', Int64, (0, None), (False, None)
		yield 'ioptional', Int64, (0, None), (False, None)
		yield 'enum', Pointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Int64Data [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
