from source.formats.base.basic import fmt_member
import numpy
from generated.context import ContextReference


class BKHDSection:

	"""
	First Section of a soundbank aux
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
		self.unk = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.unk = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

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
		instance.length = stream.read_uint()
		instance.version = stream.read_uint()
		instance.context.version = instance.version
		instance.id_a = stream.read_uint()
		instance.id_b = stream.read_uint()
		instance.constant_a = stream.read_uint()
		instance.constant_b = stream.read_uint()
		instance.unk = stream.read_uints((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.length)
		stream.write_uint(instance.version)
		stream.write_uint(instance.id_a)
		stream.write_uint(instance.id_b)
		stream.write_uint(instance.constant_a)
		stream.write_uint(instance.constant_b)
		stream.write_uints(instance.unk)

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
		return f'BKHDSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* length = {fmt_member(self.length, indent+1)}'
		s += f'\n	* version = {fmt_member(self.version, indent+1)}'
		s += f'\n	* id_a = {fmt_member(self.id_a, indent+1)}'
		s += f'\n	* id_b = {fmt_member(self.id_b, indent+1)}'
		s += f'\n	* constant_a = {fmt_member(self.constant_a, indent+1)}'
		s += f'\n	* constant_b = {fmt_member(self.constant_b, indent+1)}'
		s += f'\n	* unk = {fmt_member(self.unk, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
