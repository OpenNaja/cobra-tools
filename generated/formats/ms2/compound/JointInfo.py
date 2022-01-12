import numpy
import typing
from generated.array import Array
from generated.formats.ms2.compound.CommonJointInfo import CommonJointInfo
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry


class JointInfo(CommonJointInfo):

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 8 bytes of zeros
		self.zero = 0

		# 8 bytes of zeros per hitcheck
		self.zeros_per_hitcheck = numpy.zeros((self.hitcheck_count), dtype='uint64')
		self.hit_check = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.zero = 0
		self.zeros_per_hitcheck = numpy.zeros((self.hitcheck_count), dtype='uint64')
		self.hit_check = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.zero = stream.read_uint64()
		self.zeros_per_hitcheck = stream.read_uint64s((self.hitcheck_count))
		self.hit_check.read(stream, HitCheckEntry, self.hitcheck_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_uint64(self.zero)
		stream.write_uint64s(self.zeros_per_hitcheck)
		self.hit_check.write(stream, HitCheckEntry, self.hitcheck_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* zeros_per_hitcheck = {self.zeros_per_hitcheck.__repr__()}'
		s += f'\n	* hit_check = {self.hit_check.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
