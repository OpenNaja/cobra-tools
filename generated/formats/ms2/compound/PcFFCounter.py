import numpy
from generated.context import ContextReference


class PcFFCounter:

	"""
	count is nonzero in PZ broken birch model
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count = 0
		self.f_fs = numpy.zeros((self.count,), dtype=numpy.dtype('int8'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.count = 0
		self.f_fs = numpy.zeros((self.count,), dtype=numpy.dtype('int8'))

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
		instance.count = stream.read_uint()
		instance.f_fs = stream.read_bytes((instance.count,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.count)
		stream.write_bytes(instance.f_fs)

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
		return f'PcFFCounter [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* f_fs = {self.f_fs.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
