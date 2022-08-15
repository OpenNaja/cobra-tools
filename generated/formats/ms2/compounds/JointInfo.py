import numpy
from generated.array import Array
from generated.formats.base.basic import Uint64
from generated.formats.ms2.compounds.CommonJointInfo import CommonJointInfo
from generated.formats.ms2.compounds.HitCheckEntry import HitCheckEntry


class JointInfo(CommonJointInfo):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 8 bytes of zeros
		self.zero = 0

		# 8 bytes of zeros per hitcheck
		self.zeros_per_hitcheck = numpy.zeros((self.hitcheck_count,), dtype=numpy.dtype('uint64'))
		self.hitchecks = Array((self.hitcheck_count,), HitCheckEntry, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zero = 0
		self.zeros_per_hitcheck = numpy.zeros((self.hitcheck_count,), dtype=numpy.dtype('uint64'))
		self.hitchecks = Array((self.hitcheck_count,), HitCheckEntry, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zeros_per_hitcheck = Array.from_stream(stream, instance.context, 0, None, (instance.hitcheck_count,), Uint64)
		instance.hitchecks = Array.from_stream(stream, instance.context, 0, None, (instance.hitcheck_count,), HitCheckEntry)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.zero)
		stream.write_uint64s(instance.zeros_per_hitcheck)
		Array.to_stream(stream, instance.hitchecks, (instance.hitcheck_count,), HitCheckEntry, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zero', Uint64, (0, None)
		yield 'zeros_per_hitcheck', Array, ((instance.hitcheck_count,), Uint64, 0, None)
		yield 'hitchecks', Array, ((instance.hitcheck_count,), HitCheckEntry, 0, None)

	def get_info_str(self, indent=0):
		return f'JointInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* zeros_per_hitcheck = {self.fmt_member(self.zeros_per_hitcheck, indent+1)}'
		s += f'\n	* hitchecks = {self.fmt_member(self.hitchecks, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
