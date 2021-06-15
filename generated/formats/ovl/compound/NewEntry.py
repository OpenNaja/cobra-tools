import numpy
import typing
from generated.array import Array


class NewEntry:

	"""
	32 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# ?
		self.unks = numpy.zeros((8), dtype='uint')

	def read(self, stream):

		self.io_start = stream.tell()
		self.unks = stream.read_uints((8))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uints(self.unks)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'NewEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unks = {self.unks.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
