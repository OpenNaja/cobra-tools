import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Repeat(BaseStruct):

	__name__ = Repeat

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros_0 = Array((0,), Uint64, self.context, 0, None)

		# to be read sequentially starting after this array
		self.byte_size = 0
		self.zeros_1 = Array((0,), Uint64, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zeros_0 = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zeros_0 = Array.from_stream(stream, instance.context, 0, None, (7,), Uint64)
		instance.byte_size = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zeros_1 = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.zeros_0, (7,), Uint64, instance.context, 0, None)
		Uint64.to_stream(stream, instance.byte_size)
		Array.to_stream(stream, instance.zeros_1, (2,), Uint64, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zeros_0', Array, ((7,), Uint64, 0, None), (False, None)
		yield 'byte_size', Uint64, (0, None), (False, None)
		yield 'zeros_1', Array, ((2,), Uint64, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Repeat [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zeros_0 = {self.fmt_member(self.zeros_0, indent+1)}'
		s += f'\n	* byte_size = {self.fmt_member(self.byte_size, indent+1)}'
		s += f'\n	* zeros_1 = {self.fmt_member(self.zeros_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
