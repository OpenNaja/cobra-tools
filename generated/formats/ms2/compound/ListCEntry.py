import numpy
from generated.context import ContextReference
from generated.formats.ms2.compound.Vector3 import Vector3


class ListCEntry:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 1 for carch and nasuto
		self.one = 0

		# center of the collider
		self.loc = Vector3(self.context, 0, None)

		# -1 for PZ, 80 for JWE
		self.constant = 0.0

		# ?
		self.a = 0.0

		# ?
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))

		# sometimes repeat of a
		self.a_2 = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.one = 0
		self.loc = Vector3(self.context, 0, None)
		self.constant = 0.0
		self.a = 0.0
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.a_2 = 0.0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.one = stream.read_uint()
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
		instance.constant = stream.read_float()
		instance.a = stream.read_float()
		instance.floats = stream.read_floats((4,))
		instance.a_2 = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.one)
		Vector3.to_stream(stream, instance.loc)
		stream.write_float(instance.constant)
		stream.write_float(instance.a)
		stream.write_floats(instance.floats)
		stream.write_float(instance.a_2)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

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
