import numpy
import typing
from generated.array import Array


class MinusPadding:

	"""
	Used in PC
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# -1
		self.indices = numpy.zeros((), dtype='short')

		# 0
		self.padding = numpy.zeros((), dtype='byte')

	def read(self, stream):

		self.io_start = stream.tell()
		self.indices = stream.read_shorts((self.arg))
		self.padding = stream.read_bytes(((16 - ((self.arg * 2) % 16)) % 16))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_shorts(self.indices)
		stream.write_bytes(self.padding)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MinusPadding [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* indices = {self.indices.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
