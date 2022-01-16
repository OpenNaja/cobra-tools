import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class Info:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name_ptr = 0
		self.flags = numpy.zeros((4), dtype='byte')
		self.value = numpy.zeros((4), dtype='float')
		self.padding = 0
		self.set_defaults()

	def set_defaults(self):
		self.name_ptr = 0
		self.flags = numpy.zeros((4), dtype='byte')
		self.value = numpy.zeros((4), dtype='float')
		self.padding = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.name_ptr = stream.read_uint64()
		self.flags = stream.read_bytes((4))
		self.value = stream.read_floats((4))
		self.padding = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.name_ptr)
		stream.write_bytes(self.flags)
		stream.write_floats(self.value)
		stream.write_uint(self.padding)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Info [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_ptr = {self.name_ptr.__repr__()}'
		s += f'\n	* flags = {self.flags.__repr__()}'
		s += f'\n	* value = {self.value.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
