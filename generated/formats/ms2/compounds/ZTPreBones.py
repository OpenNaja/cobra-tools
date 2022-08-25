import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64


class ZTPreBones(BaseStruct):

	__name__ = ZTPreBones

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = Array((0,), Uint64, self.context, 0, None)
		self.unks = Array((0,), Uint, self.context, 0, None)
		self.unks_2 = Array((0,), Uint, self.context, 0, None)
		self.floats = Array((0,), Float, self.context, 0, None)
		self.unks_3 = Array((0,), Uint, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.unks = numpy.zeros((8,), dtype=numpy.dtype('uint32'))
		self.unks_2 = numpy.zeros((10,), dtype=numpy.dtype('uint32'))
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.unks_3 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zeros = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)
		instance.unks = Array.from_stream(stream, instance.context, 0, None, (8,), Uint)
		instance.unks_2 = Array.from_stream(stream, instance.context, 0, None, (10,), Uint)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (4,), Float)
		instance.unks_3 = Array.from_stream(stream, instance.context, 0, None, (2,), Uint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.zeros, (2,), Uint64, instance.context, 0, None)
		Array.to_stream(stream, instance.unks, (8,), Uint, instance.context, 0, None)
		Array.to_stream(stream, instance.unks_2, (10,), Uint, instance.context, 0, None)
		Array.to_stream(stream, instance.floats, (4,), Float, instance.context, 0, None)
		Array.to_stream(stream, instance.unks_3, (2,), Uint, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zeros', Array, ((2,), Uint64, 0, None), (False, None)
		yield 'unks', Array, ((8,), Uint, 0, None), (False, None)
		yield 'unks_2', Array, ((10,), Uint, 0, None), (False, None)
		yield 'floats', Array, ((4,), Float, 0, None), (False, None)
		yield 'unks_3', Array, ((2,), Uint, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ZTPreBones [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		s += f'\n	* unks = {self.fmt_member(self.unks, indent+1)}'
		s += f'\n	* unks_2 = {self.fmt_member(self.unks_2, indent+1)}'
		s += f'\n	* floats = {self.fmt_member(self.floats, indent+1)}'
		s += f'\n	* unks_3 = {self.fmt_member(self.unks_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
