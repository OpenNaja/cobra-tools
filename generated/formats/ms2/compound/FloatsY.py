import numpy
from generated.context import ContextReference


class FloatsY:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.floats = numpy.zeros((8), dtype=numpy.dtype('float32'))
		self.index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.floats = numpy.zeros((8), dtype=numpy.dtype('float32'))
		self.index = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.floats = stream.read_floats((8))
		self.index = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_floats(self.floats)
		stream.write_uint(self.index)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'FloatsY [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* index = {self.index.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
