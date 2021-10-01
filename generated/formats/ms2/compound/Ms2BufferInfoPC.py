import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class Ms2BufferInfoPC:

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	PC: 32 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_1 = numpy.zeros((2), dtype='uint64')

		# Total size of vertex buffer for PC, starting with the 0 - 16 byte indices
		self.vertex_buffer_size = 0
		self.zero_2 = 0
		self.set_defaults()

	def set_defaults(self):
		self.zeros_1 = numpy.zeros((2), dtype='uint64')
		self.vertex_buffer_size = 0
		self.zero_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.zeros_1 = stream.read_uint64s((2))
		self.vertex_buffer_size = stream.read_uint64()
		self.zero_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64s(self.zeros_1)
		stream.write_uint64(self.vertex_buffer_size)
		stream.write_uint64(self.zero_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BufferInfoPC [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* vertex_buffer_size = {self.vertex_buffer_size.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
