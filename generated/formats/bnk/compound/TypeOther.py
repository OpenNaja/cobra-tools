import numpy
import typing
from generated.array import Array


class TypeOther:

	"""
	generic
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of this section
		self.length = 0

		# id of this Sound SFX object
		self.raw = numpy.zeros((self.length), dtype='byte')

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.raw = stream.read_bytes((self.length))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_bytes(self.raw)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'TypeOther [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* length = {self.length.__repr__()}'
		s += f'\n	* raw = {self.raw.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
