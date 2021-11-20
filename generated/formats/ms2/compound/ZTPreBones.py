import numpy
from generated.context import ContextReference


class ZTPreBones:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros = numpy.zeros((2), dtype=numpy.dtype('uint64'))
		self.unks = numpy.zeros((8), dtype=numpy.dtype('uint32'))
		self.unks_2 = numpy.zeros((10), dtype=numpy.dtype('uint32'))
		self.floats = numpy.zeros((4), dtype=numpy.dtype('float32'))
		self.unks_3 = numpy.zeros((2), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zeros = numpy.zeros((2), dtype=numpy.dtype('uint64'))
		self.unks = numpy.zeros((8), dtype=numpy.dtype('uint32'))
		self.unks_2 = numpy.zeros((10), dtype=numpy.dtype('uint32'))
		self.floats = numpy.zeros((4), dtype=numpy.dtype('float32'))
		self.unks_3 = numpy.zeros((2), dtype=numpy.dtype('uint32'))

	def read(self, stream):
		self.io_start = stream.tell()
		self.zeros = stream.read_uint64s((2))
		self.unks = stream.read_uints((8))
		self.unks_2 = stream.read_uints((10))
		self.floats = stream.read_floats((4))
		self.unks_3 = stream.read_uints((2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64s(self.zeros)
		stream.write_uints(self.unks)
		stream.write_uints(self.unks_2)
		stream.write_floats(self.floats)
		stream.write_uints(self.unks_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ZTPreBones [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		s += f'\n	* unks_2 = {self.unks_2.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* unks_3 = {self.unks_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
