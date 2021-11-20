import numpy
from generated.context import ContextReference
from generated.formats.ms2.compound.Vector3 import Vector3


class ListCEntry:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 1 for carch and nasuto
		self.one = 0

		# center of the collider
		self.loc = Vector3(self.context, None, None)

		# -1 for PZ, 80 for JWE
		self.constant = 0.0

		# ?
		self.a = 0.0

		# ?
		self.floats = numpy.zeros((4), dtype=numpy.dtype('float32'))

		# sometimes repeat of a
		self.a_2 = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.one = 0
		self.loc = Vector3(self.context, None, None)
		self.constant = 0.0
		self.a = 0.0
		self.floats = numpy.zeros((4), dtype=numpy.dtype('float32'))
		self.a_2 = 0.0

	def read(self, stream):
		self.io_start = stream.tell()
		self.one = stream.read_uint()
		self.loc = stream.read_type(Vector3, (self.context, None, None))
		self.constant = stream.read_float()
		self.a = stream.read_float()
		self.floats = stream.read_floats((4))
		self.a_2 = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.one)
		stream.write_type(self.loc)
		stream.write_float(self.constant)
		stream.write_float(self.a)
		stream.write_floats(self.floats)
		stream.write_float(self.a_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListCEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* loc = {self.loc.__repr__()}'
		s += f'\n	* constant = {self.constant.__repr__()}'
		s += f'\n	* a = {self.a.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* a_2 = {self.a_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
