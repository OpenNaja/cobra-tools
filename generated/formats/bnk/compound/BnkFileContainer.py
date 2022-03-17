import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString


class BnkFileContainer:

	"""
	Buffer data of bnk files
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# data size of aux file of type b
		self.size_b = 0

		# 1, guess
		self.name_count = 0

		# 2 for PZ, 6 for ZTUAC
		self.count_2 = 0

		# variable
		self.stream_info_count = 0

		# 0
		self.zeros = numpy.zeros((7,), dtype=numpy.dtype('uint32'))

		# 0
		self.zeros_2 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

		# data
		self.stream_infos = numpy.zeros((self.stream_info_count, 3,), dtype=numpy.dtype('uint64'))

		# data
		self.names = Array((self.name_count,), ZString, self.context, 0, None)

		# ext format subtypes
		self.extensions = Array((self.count_2,), ZString, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.size_b = 0
		self.name_count = 0
		self.count_2 = 0
		self.stream_info_count = 0
		self.zeros = numpy.zeros((7,), dtype=numpy.dtype('uint32'))
		if (self.context.user_version.is_jwe and (self.context.version == 19)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.zeros_2 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.stream_infos = numpy.zeros((self.stream_info_count, 3,), dtype=numpy.dtype('uint64'))
		self.names = Array((self.name_count,), ZString, self.context, 0, None)
		self.extensions = Array((self.count_2,), ZString, self.context, 0, None)

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
		instance.size_b = stream.read_uint64()
		instance.name_count = stream.read_uint()
		instance.count_2 = stream.read_uint()
		instance.stream_info_count = stream.read_uint()
		instance.zeros = stream.read_uints((7,))
		if (instance.context.user_version.is_jwe and (instance.context.version == 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			instance.zeros_2 = stream.read_uints((2,))
		instance.stream_infos = stream.read_uint64s((instance.stream_info_count, 3,))
		instance.names = stream.read_zstrings((instance.name_count,))
		instance.extensions = stream.read_zstrings((instance.count_2,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.size_b)
		stream.write_uint(instance.name_count)
		stream.write_uint(instance.count_2)
		stream.write_uint(instance.stream_info_count)
		stream.write_uints(instance.zeros)
		if (instance.context.user_version.is_jwe and (instance.context.version == 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			stream.write_uints(instance.zeros_2)
		stream.write_uint64s(instance.stream_infos)
		stream.write_zstrings(instance.names)
		stream.write_zstrings(instance.extensions)

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
		return f'BnkFileContainer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* size_b = {self.size_b.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* count_2 = {self.count_2.__repr__()}'
		s += f'\n	* stream_info_count = {self.stream_info_count.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* stream_infos = {self.stream_infos.__repr__()}'
		s += f'\n	* names = {self.names.__repr__()}'
		s += f'\n	* extensions = {self.extensions.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
