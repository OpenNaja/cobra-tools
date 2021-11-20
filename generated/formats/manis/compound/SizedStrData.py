import numpy
from generated.context import ContextReference


class SizedStrData:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.hash_block_size = 0
		self.zeros = numpy.zeros((2), dtype=numpy.dtype('int32'))
		self.c_1 = 0
		self.zeros_end = numpy.zeros((9), dtype=numpy.dtype('uint16'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.a = 0
		self.hash_block_size = 0
		self.zeros = numpy.zeros((2), dtype=numpy.dtype('int32'))
		self.c_1 = 0
		if (not self.context.user_version.is_jwe) and (self.context.version == 20):
			self.zeros_end = numpy.zeros((9), dtype=numpy.dtype('uint16'))

	def read(self, stream):
		self.io_start = stream.tell()
		self.a = stream.read_ushort()
		self.hash_block_size = stream.read_ushort()
		self.zeros = stream.read_ints((2))
		self.c_1 = stream.read_ushort()
		if (not self.context.user_version.is_jwe) and (self.context.version == 20):
			self.zeros_end = stream.read_ushorts((9))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_ushort(self.a)
		stream.write_ushort(self.hash_block_size)
		stream.write_ints(self.zeros)
		stream.write_ushort(self.c_1)
		if (not self.context.user_version.is_jwe) and (self.context.version == 20):
			stream.write_ushorts(self.zeros_end)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* a = {self.a.__repr__()}'
		s += f'\n	* hash_block_size = {self.hash_block_size.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* c_1 = {self.c_1.__repr__()}'
		s += f'\n	* zeros_end = {self.zeros_end.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
