import numpy
from generated.context import ContextReference


class Repeat:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_0 = numpy.zeros((14), dtype=numpy.dtype('uint32'))

		# to be read sequentially starting after this array
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((5), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zeros_0 = numpy.zeros((14), dtype=numpy.dtype('uint32'))
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((5), dtype=numpy.dtype('uint32'))

	def read(self, stream):
		self.io_start = stream.tell()
		self.zeros_0 = stream.read_uints((14))
		self.byte_size = stream.read_uint()
		self.zeros_1 = stream.read_uints((5))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uints(self.zeros_0)
		stream.write_uint(self.byte_size)
		stream.write_uints(self.zeros_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Repeat [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* byte_size = {self.byte_size.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
