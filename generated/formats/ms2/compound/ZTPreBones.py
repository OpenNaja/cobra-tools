from source.formats.base.basic import fmt_member
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
		self.zeros = 0
		self.unks = 0
		self.unks_2 = 0
		self.floats = 0
		self.unks_3 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.unks = numpy.zeros((8,), dtype=numpy.dtype('uint32'))
		self.unks_2 = numpy.zeros((10,), dtype=numpy.dtype('uint32'))
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.unks_3 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

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
		instance.zeros = stream.read_uint64s((2,))
		instance.unks = stream.read_uints((8,))
		instance.unks_2 = stream.read_uints((10,))
		instance.floats = stream.read_floats((4,))
		instance.unks_3 = stream.read_uints((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64s(instance.zeros)
		stream.write_uints(instance.unks)
		stream.write_uints(instance.unks_2)
		stream.write_floats(instance.floats)
		stream.write_uints(instance.unks_3)

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

	def get_info_str(self, indent=0):
		return f'ZTPreBones [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* zeros = {fmt_member(self.zeros, indent+1)}'
		s += f'\n	* unks = {fmt_member(self.unks, indent+1)}'
		s += f'\n	* unks_2 = {fmt_member(self.unks_2, indent+1)}'
		s += f'\n	* floats = {fmt_member(self.floats, indent+1)}'
		s += f'\n	* unks_3 = {fmt_member(self.unks_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
