import numpy
from generated.array import Array
from generated.formats.ms2.compound.CommonJointInfo import CommonJointInfo
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry


class JointInfo(CommonJointInfo):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 8 bytes of zeros
		self.zero = 0

		# 8 bytes of zeros per hitcheck
		self.zeros_per_hitcheck = numpy.zeros((self.hitcheck_count,), dtype=numpy.dtype('uint64'))
		self.hitchecks = Array((self.hitcheck_count,), HitCheckEntry, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zero = 0
		self.zeros_per_hitcheck = numpy.zeros((self.hitcheck_count,), dtype=numpy.dtype('uint64'))
		self.hitchecks = Array((self.hitcheck_count,), HitCheckEntry, self.context, 0, None)

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
		instance.zero = stream.read_uint64()
		instance.zeros_per_hitcheck = stream.read_uint64s((instance.hitcheck_count,))
		instance.hitchecks = Array.from_stream(stream, (instance.hitcheck_count,), HitCheckEntry, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.zero)
		stream.write_uint64s(instance.zeros_per_hitcheck)
		Array.to_stream(stream, instance.hitchecks, (instance.hitcheck_count,), HitCheckEntry, instance.context, 0, None)

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
		return f'JointInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* zeros_per_hitcheck = {self.zeros_per_hitcheck.__repr__()}'
		s += f'\n	* hitchecks = {self.hitchecks.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
