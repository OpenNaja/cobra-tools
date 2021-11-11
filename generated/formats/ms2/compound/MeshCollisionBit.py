import numpy
from generated.array import Array
from generated.context import ContextReference


class MeshCollisionBit:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# ?
		self.countd = numpy.zeros((34), dtype='ushort')

		# always 2954754766?
		self.consts = numpy.zeros((3), dtype='uint')
		self.set_defaults()

	def set_defaults(self):
		self.countd = numpy.zeros((34), dtype='ushort')
		self.consts = numpy.zeros((3), dtype='uint')

	def read(self, stream):
		self.io_start = stream.tell()
		self.countd = stream.read_ushorts((34))
		self.consts = stream.read_uints((3))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_ushorts(self.countd)
		stream.write_uints(self.consts)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MeshCollisionBit [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* countd = {self.countd.__repr__()}'
		s += f'\n	* consts = {self.consts.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
