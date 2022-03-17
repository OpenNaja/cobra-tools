import numpy
from generated.context import ContextReference


class CommonJointInfo:

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

		# bunch of -1's
		self.f_fs = numpy.zeros((3,), dtype=numpy.dtype('int32'))
		self.name_offset = 0
		self.hitcheck_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.eleven = 0
		self.f_fs = numpy.zeros((3,), dtype=numpy.dtype('int32'))
		self.name_offset = 0
		self.hitcheck_count = 0

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
		instance.f_fs = stream.read_ints((3,))
		instance.name_offset = stream.read_uint()
		instance.hitcheck_count = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.eleven)
		stream.write_ints(instance.f_fs)
		stream.write_uint(instance.name_offset)
		stream.write_uint(instance.hitcheck_count)

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
		return f'CommonJointInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* eleven = {self.eleven.__repr__()}'
		s += f'\n	* f_fs = {self.f_fs.__repr__()}'
		s += f'\n	* name_offset = {self.name_offset.__repr__()}'
		s += f'\n	* hitcheck_count = {self.hitcheck_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
