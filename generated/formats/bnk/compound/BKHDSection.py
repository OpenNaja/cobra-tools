import numpy
from generated.context import ContextReference


class BKHDSection:

	"""
	First Section of a soundback aux
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.unk = numpy.zeros((2), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.unk = numpy.zeros((2), dtype=numpy.dtype('uint32'))

	def read(self, stream):
		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.version = stream.read_uint()
		self.context.version = self.version
		self.id_a = stream.read_uint()
		self.id_b = stream.read_uint()
		self.constant_a = stream.read_uint()
		self.constant_b = stream.read_uint()
		self.unk = stream.read_uints((2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_uint(self.version)
		stream.write_uint(self.id_a)
		stream.write_uint(self.id_b)
		stream.write_uint(self.constant_a)
		stream.write_uint(self.constant_b)
		stream.write_uints(self.unk)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BKHDSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* length = {self.length.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* id_a = {self.id_a.__repr__()}'
		s += f'\n	* id_b = {self.id_b.__repr__()}'
		s += f'\n	* constant_a = {self.constant_a.__repr__()}'
		s += f'\n	* constant_b = {self.constant_b.__repr__()}'
		s += f'\n	* unk = {self.unk.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
