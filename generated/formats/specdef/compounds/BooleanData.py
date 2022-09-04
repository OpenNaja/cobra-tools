import numpy
from generated.array import Array
from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BooleanData(MemStruct):

	"""
	8 bytes in log
	"""

	__name__ = 'BooleanData'

	_import_path = 'generated.formats.specdef.compounds.BooleanData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = 0
		self.default = 0
		self.unused = Array(self.context, 0, None, (0,), Ubyte)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.value = 0
		self.default = 0
		self.unused = numpy.zeros((6,), dtype=numpy.dtype('uint8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.value = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.default = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.unused = Array.from_stream(stream, instance.context, 0, None, (6,), Ubyte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ubyte.to_stream(stream, instance.value)
		Ubyte.to_stream(stream, instance.default)
		Array.to_stream(stream, instance.unused, instance.context, 0, None, (6,), Ubyte)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'value', Ubyte, (0, None), (False, None)
		yield 'default', Ubyte, (0, None), (False, None)
		yield 'unused', Array, (0, None, (6,), Ubyte), (False, None)

	def get_info_str(self, indent=0):
		return f'BooleanData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* value = {self.fmt_member(self.value, indent+1)}'
		s += f'\n	* default = {self.fmt_member(self.default, indent+1)}'
		s += f'\n	* unused = {self.fmt_member(self.unused, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
