import numpy
from generated.context import ContextReference


class Repeat:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_0 = numpy.zeros((7,), dtype=numpy.dtype('uint64'))

		# to be read sequentially starting after this array
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zeros_0 = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

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
		instance.zeros_0 = stream.read_uint64s((7,))
		instance.byte_size = stream.read_uint64()
		instance.zeros_1 = stream.read_uint64s((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64s(instance.zeros_0)
		stream.write_uint64(instance.byte_size)
		stream.write_uint64s(instance.zeros_1)

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
