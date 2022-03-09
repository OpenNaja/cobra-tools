import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class Repeat:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_0 = numpy.zeros((7), dtype='uint64')

		# to be read sequentially starting after this array
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((2), dtype='uint64')
		self.set_defaults()

	def set_defaults(self):
		self.zeros_0 = numpy.zeros((7), dtype='uint64')
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((2), dtype='uint64')

	def read(self, stream):
		self.io_start = stream.tell()
		self.zeros_0 = stream.read_uint64s((7))
		self.byte_size = stream.read_uint64()
		self.zeros_1 = stream.read_uint64s((2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64s(self.zeros_0)
		stream.write_uint64(self.byte_size)
		stream.write_uint64s(self.zeros_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Repeat [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* byte_size = {self.byte_size.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
