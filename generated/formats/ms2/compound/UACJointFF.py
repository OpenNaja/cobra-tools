from source.formats.base.basic import fmt_member
import numpy
from generated.context import ContextReference


class UACJointFF:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# must be 11
		self.eleven = 0

		# bunch of -1's, and constants
		self.f_fs = numpy.zeros((4,), dtype=numpy.dtype('int32'))
		self.name_offset = 0
		self.hitcheck_count = 0

		# 12 bytes of zeros
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.eleven = 0
		self.f_fs = numpy.zeros((4,), dtype=numpy.dtype('int32'))
		self.name_offset = 0
		self.hitcheck_count = 0
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

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
		instance.eleven = stream.read_uint()
		instance.f_fs = stream.read_ints((4,))
		instance.name_offset = stream.read_uint()
		instance.hitcheck_count = stream.read_uint()
		instance.zeros = stream.read_uints((3,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.eleven)
		stream.write_ints(instance.f_fs)
		stream.write_uint(instance.name_offset)
		stream.write_uint(instance.hitcheck_count)
		stream.write_uints(instance.zeros)

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
		return f'UACJointFF [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* eleven = {fmt_member(self.eleven, indent+1)}'
		s += f'\n	* f_fs = {fmt_member(self.f_fs, indent+1)}'
		s += f'\n	* name_offset = {fmt_member(self.name_offset, indent+1)}'
		s += f'\n	* hitcheck_count = {fmt_member(self.hitcheck_count, indent+1)}'
		s += f'\n	* zeros = {fmt_member(self.zeros, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
