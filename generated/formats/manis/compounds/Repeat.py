import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Repeat(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros_0 = 0

		# to be read sequentially starting after this array
		self.byte_size = 0
		self.zeros_1 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zeros_0 = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zeros_0 = stream.read_uint64s((7,))
		instance.byte_size = stream.read_uint64()
		instance.zeros_1 = stream.read_uint64s((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64s(instance.zeros_0)
		stream.write_uint64(instance.byte_size)
		stream.write_uint64s(instance.zeros_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('zeros_0', Array, ((7,), Uint64, 0, None))
		yield ('byte_size', Uint64, (0, None))
		yield ('zeros_1', Array, ((2,), Uint64, 0, None))

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
