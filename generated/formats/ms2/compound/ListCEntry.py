import numpy
import typing
from generated.array import Array


class ListCEntry:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 1 for carch and nasuto
		self.one = 0

		# ?
		self.floats = numpy.zeros((10), dtype='float')

	def read(self, stream):

		self.io_start = stream.tell()
		self.one = stream.read_uint()
		self.floats = stream.read_floats((10))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.one)
		stream.write_floats(self.floats)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListCEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
