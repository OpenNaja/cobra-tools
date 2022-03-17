import numpy
from generated.context import ContextReference


class Ms2SizedStrData:

	"""
	Seems to be the 'root header' of the ms2.
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# see version tag
		self.version = 0

		# 1 if yes, 0 if no
		self.vertex_buffer_count = 0
		self.mdl_2_count = 0

		# count of names in ms2 buffer0
		self.name_count = 0

		# usually 0, rarely 1
		self.unk_count = 0

		# seems to be zeros
		self.unknown_1 = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

		# 8 empty bytes
		self.ptr_0 = 0

		# 8 empty bytes
		self.ptr_1 = 0

		# 8 empty bytes
		self.ptr_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.version = 0
		self.vertex_buffer_count = 0
		self.mdl_2_count = 0
		self.name_count = 0
		self.unk_count = 0
		self.unknown_1 = numpy.zeros((3,), dtype=numpy.dtype('uint32'))
		self.ptr_0 = 0
		self.ptr_1 = 0
		self.ptr_2 = 0

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
		instance.version = stream.read_uint()
		instance.context.version = instance.version
		instance.vertex_buffer_count = stream.read_ushort()
		instance.mdl_2_count = stream.read_ushort()
		instance.name_count = stream.read_ushort()
		instance.unk_count = stream.read_ushort()
		instance.unknown_1 = stream.read_uints((3,))
		instance.ptr_0 = stream.read_uint64()
		instance.ptr_1 = stream.read_uint64()
		instance.ptr_2 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.version)
		stream.write_ushort(instance.vertex_buffer_count)
		stream.write_ushort(instance.mdl_2_count)
		stream.write_ushort(instance.name_count)
		stream.write_ushort(instance.unk_count)
		stream.write_uints(instance.unknown_1)
		stream.write_uint64(instance.ptr_0)
		stream.write_uint64(instance.ptr_1)
		stream.write_uint64(instance.ptr_2)

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
		return f'Ms2SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* vertex_buffer_count = {self.vertex_buffer_count.__repr__()}'
		s += f'\n	* mdl_2_count = {self.mdl_2_count.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* unk_count = {self.unk_count.__repr__()}'
		s += f'\n	* unknown_1 = {self.unknown_1.__repr__()}'
		s += f'\n	* ptr_0 = {self.ptr_0.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
