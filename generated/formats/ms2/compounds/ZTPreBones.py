import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64


class ZTPreBones(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.unks = numpy.zeros((8,), dtype=numpy.dtype('uint32'))
		self.unks_2 = numpy.zeros((10,), dtype=numpy.dtype('uint32'))
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.unks_3 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
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
		instance.zeros = stream.read_uint64s((2,))
		instance.unks = stream.read_uints((8,))
		instance.unks_2 = stream.read_uints((10,))
		instance.floats = stream.read_floats((4,))
		instance.unks_3 = stream.read_uints((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64s(instance.zeros)
		stream.write_uints(instance.unks)
		stream.write_uints(instance.unks_2)
		stream.write_floats(instance.floats)
		stream.write_uints(instance.unks_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zeros', Array, ((2,), Uint64, 0, None)
		yield 'unks', Array, ((8,), Uint, 0, None)
		yield 'unks_2', Array, ((10,), Uint, 0, None)
		yield 'floats', Array, ((4,), Float, 0, None)
		yield 'unks_3', Array, ((2,), Uint, 0, None)

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
