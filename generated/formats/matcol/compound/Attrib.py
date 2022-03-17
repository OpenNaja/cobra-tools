import numpy
from generated.context import ContextReference


class Attrib:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name_ptr = 0
		self.attrib = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.padding = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.name_ptr = 0
		self.attrib = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.padding = 0

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
		instance.name_ptr = stream.read_uint64()
		instance.attrib = stream.read_bytes((4,))
		instance.padding = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.name_ptr)
		stream.write_bytes(instance.attrib)
		stream.write_uint(instance.padding)

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
		return f'Attrib [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_ptr = {self.name_ptr.__repr__()}'
		s += f'\n	* attrib = {self.attrib.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
