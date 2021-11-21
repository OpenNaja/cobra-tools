import numpy
from generated.context import ContextReference


class SizedStrData:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.hash_block_size = 0
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('int32'))
		self.c_1 = 0
		self.zeros_end = numpy.zeros((9,), dtype=numpy.dtype('uint16'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.a = 0
		self.hash_block_size = 0
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('int32'))
		self.c_1 = 0
		if (not self.context.user_version.is_jwe) and (self.context.version == 20):
			self.zeros_end = numpy.zeros((9,), dtype=numpy.dtype('uint16'))

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
		instance.a = stream.read_ushort()
		instance.hash_block_size = stream.read_ushort()
		instance.zeros = stream.read_ints((2,))
		instance.c_1 = stream.read_ushort()
		if (not instance.context.user_version.is_jwe) and (instance.context.version == 20):
			instance.zeros_end = stream.read_ushorts((9,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ushort(instance.a)
		stream.write_ushort(instance.hash_block_size)
		stream.write_ints(instance.zeros)
		stream.write_ushort(instance.c_1)
		if (not instance.context.user_version.is_jwe) and (instance.context.version == 20):
			stream.write_ushorts(instance.zeros_end)

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
