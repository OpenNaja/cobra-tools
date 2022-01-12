import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class UACJoint:

	"""
	36 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# variable
		self.unk = numpy.zeros((6), dtype='ushort')

		# some at least
		self.floats = numpy.zeros((6), dtype='float')
		self.set_defaults()

	def set_defaults(self):
		self.unk = numpy.zeros((6), dtype='ushort')
		self.floats = numpy.zeros((6), dtype='float')

	def read(self, stream):
		self.io_start = stream.tell()
		self.unk = stream.read_ushorts((6))
		self.floats = stream.read_floats((6))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_ushorts(self.unk)
		stream.write_floats(self.floats)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'UACJoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unk = {self.unk.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
