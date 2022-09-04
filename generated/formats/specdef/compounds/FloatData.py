from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FloatData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = 'FloatData'

	_import_path = 'generated.formats.specdef.compounds.FloatData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = 0.0
		self.imax = 0.0
		self.ivalue = 0.0
		self.ioptional = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.imin = 0.0
		self.imax = 0.0
		self.ivalue = 0.0
		self.ioptional = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.imin = Float.from_stream(stream, instance.context, 0, None)
		instance.imax = Float.from_stream(stream, instance.context, 0, None)
		instance.ivalue = Float.from_stream(stream, instance.context, 0, None)
		instance.ioptional = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.imin)
		Float.to_stream(stream, instance.imax)
		Float.to_stream(stream, instance.ivalue)
		Uint.to_stream(stream, instance.ioptional)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'imin', Float, (0, None), (False, None)
		yield 'imax', Float, (0, None), (False, None)
		yield 'ivalue', Float, (0, None), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FloatData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
