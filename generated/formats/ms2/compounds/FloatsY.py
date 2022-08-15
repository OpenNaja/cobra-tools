import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint


class FloatsY(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.floats = numpy.zeros((8,), dtype=numpy.dtype('float32'))
		self.index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.floats = numpy.zeros((8,), dtype=numpy.dtype('float32'))
		self.index = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (8,), Float)
		instance.index = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.floats, (8,), Float, instance.context, 0, None)
		Uint.to_stream(stream, instance.index)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'floats', Array, ((8,), Float, 0, None)
		yield 'index', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'FloatsY [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* floats = {self.fmt_member(self.floats, indent+1)}'
		s += f'\n	* index = {self.fmt_member(self.index, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
