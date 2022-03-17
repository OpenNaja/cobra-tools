import numpy
from generated.context import ContextReference


class UncompressedRegion:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_0 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.unk_0 = 0
		self.unk_1 = 0
		self.zeros_1 = numpy.zeros((3,), dtype=numpy.dtype('uint32'))
		self.unk_2 = 0
		self.unk_3 = 0
		self.zeros_2 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.unk_4 = 0
		self.unk_5 = 0
		self.zeros_3 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zeros_0 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.unk_0 = 0
		self.unk_1 = 0
		self.zeros_1 = numpy.zeros((3,), dtype=numpy.dtype('uint32'))
		self.unk_2 = 0
		self.unk_3 = 0
		self.zeros_2 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.unk_4 = 0
		self.unk_5 = 0
		self.zeros_3 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

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
		instance.zeros_0 = stream.read_uints((2,))
		instance.unk_0 = stream.read_ushort()
		instance.unk_1 = stream.read_ushort()
		instance.zeros_1 = stream.read_uints((3,))
		instance.unk_2 = stream.read_uint()
		instance.unk_3 = stream.read_uint()
		instance.zeros_2 = stream.read_uints((2,))
		instance.unk_4 = stream.read_uint()
		instance.unk_5 = stream.read_uint()
		instance.zeros_3 = stream.read_uints((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uints(instance.zeros_0)
		stream.write_ushort(instance.unk_0)
		stream.write_ushort(instance.unk_1)
		stream.write_uints(instance.zeros_1)
		stream.write_uint(instance.unk_2)
		stream.write_uint(instance.unk_3)
		stream.write_uints(instance.zeros_2)
		stream.write_uint(instance.unk_4)
		stream.write_uint(instance.unk_5)
		stream.write_uints(instance.zeros_3)

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
		return f'UncompressedRegion [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* unk_0 = {self.unk_0.__repr__()}'
		s += f'\n	* unk_1 = {self.unk_1.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* unk_2 = {self.unk_2.__repr__()}'
		s += f'\n	* unk_3 = {self.unk_3.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* unk_4 = {self.unk_4.__repr__()}'
		s += f'\n	* unk_5 = {self.unk_5.__repr__()}'
		s += f'\n	* zeros_3 = {self.zeros_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
