import numpy
import typing
from generated.array import Array


class BKHDSection:

	"""
	First Section of a soundback aux
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0

		# filler zeroes
		self.zeroes = numpy.zeros((self.length - 20), dtype='byte')

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.version = stream.read_uint()
		stream.version = self.version
		self.id_a = stream.read_uint()
		self.id_b = stream.read_uint()
		self.constant_a = stream.read_uint()
		self.constant_b = stream.read_uint()
		self.zeroes = stream.read_bytes((self.length - 20))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.id_a)
		stream.write_uint(self.id_b)
		stream.write_uint(self.constant_a)
		stream.write_uint(self.constant_b)
		stream.write_bytes(self.zeroes)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BKHDSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* length = {self.length.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* id_a = {self.id_a.__repr__()}'
		s += f'\n	* id_b = {self.id_b.__repr__()}'
		s += f'\n	* constant_a = {self.constant_a.__repr__()}'
		s += f'\n	* constant_b = {self.constant_b.__repr__()}'
		s += f'\n	* zeroes = {self.zeroes.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
