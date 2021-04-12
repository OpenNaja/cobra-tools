import numpy
import typing
from generated.array import Array


class SizedStrData:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.hash_block_size = 0
		self.zeros = numpy.zeros((2), dtype='int')
		self.c = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.a = stream.read_ushort()
		self.hash_block_size = stream.read_ushort()
		self.zeros = stream.read_ints((2))
		self.c = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.a)
		stream.write_ushort(self.hash_block_size)
		stream.write_ints(self.zeros)
		stream.write_ushort(self.c)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* a = {self.a.__repr__()}'
		s += f'\n	* hash_block_size = {self.hash_block_size.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* c = {self.c.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
