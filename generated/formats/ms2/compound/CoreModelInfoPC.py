import numpy
from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo


class CoreModelInfoPC(CoreModelInfo):

	"""
	152 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros = numpy.zeros((5,), dtype=numpy.dtype('uint64'))
		self.zeros = numpy.zeros((9,), dtype=numpy.dtype('uint64'))
		self.one = 0
		self.zero = 0
		self.zero_zt = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version == 18:
			self.zeros = numpy.zeros((5,), dtype=numpy.dtype('uint64'))
		if self.context.version == 17:
			self.zeros = numpy.zeros((9,), dtype=numpy.dtype('uint64'))
		self.one = 0
		self.zero = 0
		if self.context.version == 17:
			self.zero_zt = 0

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
		super().read_fields(stream, instance)
		if instance.context.version == 18:
			instance.zeros = stream.read_uint64s((5,))
		if instance.context.version == 17:
			instance.zeros = stream.read_uint64s((9,))
		instance.one = stream.read_uint64()
		instance.zero = stream.read_uint64()
		if instance.context.version == 17:
			instance.zero_zt = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version == 18:
			stream.write_uint64s(instance.zeros)
		if instance.context.version == 17:
			stream.write_uint64s(instance.zeros)
		stream.write_uint64(instance.one)
		stream.write_uint64(instance.zero)
		if instance.context.version == 17:
			stream.write_uint64(instance.zero_zt)

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
		return f'CoreModelInfoPC [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* zero_zt = {self.zero_zt.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
