import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class UnknownEntry:

	"""
	Description of one file type
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# ?
		self.unknowns = numpy.zeros((2, 2), dtype='ushort')
		self.zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknowns = stream.read_ushorts((2, 2))
		self.zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushorts(self.unknowns)
		stream.write_uint(self.zero)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'UnknownEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unknowns = {self.unknowns.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
