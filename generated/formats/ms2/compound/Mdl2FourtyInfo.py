import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class Mdl2FourtyInfo:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 0, 1 or 0, 0, 0, 0
		self.unknowns = numpy.zeros((5), dtype='uint64')

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknowns = stream.read_uint64s((5))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64s(self.unknowns)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mdl2FourtyInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unknowns = {self.unknowns.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
