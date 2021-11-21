import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry


class Struct7:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.count_7 = 0

		# seen 0
		self.zero = 0

		# only for recent versions of PZ
		self.zeros_pz = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

		# 60 bytes per entry
		self.unknown_list = Array((self.count_7,), NasutoJointEntry, self.context, 0, None)

		# align list to multiples of 8
		self.padding = numpy.zeros(((8 - ((self.count_7 * 60) % 8)) % 8,), dtype=numpy.dtype('uint8'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.count_7 = 0
		self.zero = 0
		if ((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.zeros_pz = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.unknown_list = Array((self.count_7,), NasutoJointEntry, self.context, 0, None)
		self.padding = numpy.zeros(((8 - ((self.count_7 * 60) % 8)) % 8,), dtype=numpy.dtype('uint8'))

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
		instance.count_7 = stream.read_uint64()
		instance.zero = stream.read_uint64()
		if ((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			instance.zeros_pz = stream.read_uint64s((2,))
		instance.unknown_list = Array.from_stream(stream, (instance.count_7,), NasutoJointEntry, instance.context, 0, None)
		instance.padding = stream.read_ubytes(((8 - ((instance.count_7 * 60) % 8)) % 8,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.count_7)
		stream.write_uint64(instance.zero)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			stream.write_uint64s(instance.zeros_pz)
		Array.to_stream(stream, instance.unknown_list, (instance.count_7,),NasutoJointEntry, instance.context, 0, None)
		stream.write_ubytes(instance.padding)

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
		return f'Struct7 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* zeros_pz = {self.zeros_pz.__repr__()}'
		s += f'\n	* unknown_list = {self.unknown_list.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
