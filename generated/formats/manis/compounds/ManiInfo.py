import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort


class ManiInfo(BaseStruct):

	"""
	288 bytes for JWE / PZ
	304 bytes for PC
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.duration = 0.0
		self.frame_count = 0

		# ?
		self.b = 0
		self.zeros_0 = Array((0,), Ushort, self.context, 0, None)
		self.extra_pc_1 = 0
		self.pos_bone_count = 0
		self.ori_bone_count = 0

		# likely
		self.scl_bone_count = 0

		# zero
		self.extra_pc = 0
		self.pos_bone_count_repeat = 0
		self.ori_bone_count_repeat = 0
		self.scl_bone_count_repeat = 0
		self.zeros_1 = 0
		self.zeros_1_new = 0
		self.float_count = 0

		# FF if unused
		self.count_a = 0

		# FF if unused
		self.count_b = 0

		# usually matches ms2 bone count, at least for JWE2 dinos. Doesn't match for PZ water wheel 5 vs ms2 2
		self.target_bone_count = 0

		# zero
		self.g = 0

		# rest 228 bytes
		self.zeros_2 = Array((0,), Uint, self.context, 0, None)

		# rest 14 bytes
		self.extra_zeros_pc = Array((0,), Ushort, self.context, 0, None)
		self.pos_bone_min = 0
		self.pos_bone_max = 0
		self.ori_bone_min = 0
		self.ori_bone_max = 0

		# always FF
		self.scl_bone_min = 0

		# always 00
		self.scl_bone_max = 0
		self.pos_bone_count_related = 0
		self.pos_bone_count_repeat = 0
		self.ori_bone_count_related = 0
		self.ori_bone_count_repeat = 0

		# maybe, not observed yet
		self.scl_bone_count_related = 0
		self.scl_bone_count_repeat = 0
		self.zeros_end = 0
		self.zero_2_end = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.duration = 0.0
		self.frame_count = 0
		self.b = 0
		self.zeros_0 = numpy.zeros((6,), dtype=numpy.dtype('uint16'))
		if self.context.version == 18:
			self.extra_pc_1 = 0
		self.pos_bone_count = 0
		self.ori_bone_count = 0
		self.scl_bone_count = 0
		if self.context.version == 18:
			self.extra_pc = 0
			self.pos_bone_count_repeat = 0
			self.ori_bone_count_repeat = 0
			self.scl_bone_count_repeat = 0
		self.zeros_1 = 0
		if not (self.context.version == 18):
			self.zeros_1_new = 0
		self.float_count = 0
		self.count_a = 0
		self.count_b = 0
		self.target_bone_count = 0
		self.g = 0
		self.zeros_2 = numpy.zeros((57,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.extra_zeros_pc = numpy.zeros((6,), dtype=numpy.dtype('uint16'))
		self.pos_bone_min = 0
		self.pos_bone_max = 0
		self.ori_bone_min = 0
		self.ori_bone_max = 0
		self.scl_bone_min = 0
		self.scl_bone_max = 0
		if not (self.context.version == 18):
			self.pos_bone_count_related = 0
			self.pos_bone_count_repeat = 0
			self.ori_bone_count_related = 0
			self.ori_bone_count_repeat = 0
			self.scl_bone_count_related = 0
			self.scl_bone_count_repeat = 0
			self.zeros_end = 0
		self.zero_2_end = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.duration = Float.from_stream(stream, instance.context, 0, None)
		instance.frame_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.b = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros_0 = Array.from_stream(stream, instance.context, 0, None, (6,), Ushort)
		if instance.context.version == 18:
			instance.extra_pc_1 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.pos_bone_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.ori_bone_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.scl_bone_count = Ushort.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 18:
			instance.extra_pc = Uint64.from_stream(stream, instance.context, 0, None)
			instance.pos_bone_count_repeat = Ushort.from_stream(stream, instance.context, 0, None)
			instance.ori_bone_count_repeat = Ushort.from_stream(stream, instance.context, 0, None)
			instance.scl_bone_count_repeat = Ushort.from_stream(stream, instance.context, 0, None)
		instance.zeros_1 = Ushort.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.zeros_1_new = Uint.from_stream(stream, instance.context, 0, None)
		instance.float_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.count_a = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_b = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.target_bone_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.g = Ushort.from_stream(stream, instance.context, 0, None)
		instance.zeros_2 = Array.from_stream(stream, instance.context, 0, None, (57,), Uint)
		if instance.context.version == 18:
			instance.extra_zeros_pc = Array.from_stream(stream, instance.context, 0, None, (6,), Ushort)
		instance.pos_bone_min = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.pos_bone_max = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.ori_bone_min = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.ori_bone_max = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.scl_bone_min = Byte.from_stream(stream, instance.context, 0, None)
		instance.scl_bone_max = Byte.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.pos_bone_count_related = Ubyte.from_stream(stream, instance.context, 0, None)
			instance.pos_bone_count_repeat = Ubyte.from_stream(stream, instance.context, 0, None)
			instance.ori_bone_count_related = Ubyte.from_stream(stream, instance.context, 0, None)
			instance.ori_bone_count_repeat = Ubyte.from_stream(stream, instance.context, 0, None)
			instance.scl_bone_count_related = Byte.from_stream(stream, instance.context, 0, None)
			instance.scl_bone_count_repeat = Byte.from_stream(stream, instance.context, 0, None)
			instance.zeros_end = Ushort.from_stream(stream, instance.context, 0, None)
		instance.zero_2_end = Ushort.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.duration)
		Uint.to_stream(stream, instance.frame_count)
		Uint.to_stream(stream, instance.b)
		Array.to_stream(stream, instance.zeros_0, (6,), Ushort, instance.context, 0, None)
		if instance.context.version == 18:
			Ushort.to_stream(stream, instance.extra_pc_1)
		Ushort.to_stream(stream, instance.pos_bone_count)
		Ushort.to_stream(stream, instance.ori_bone_count)
		Ushort.to_stream(stream, instance.scl_bone_count)
		if instance.context.version == 18:
			Uint64.to_stream(stream, instance.extra_pc)
			Ushort.to_stream(stream, instance.pos_bone_count_repeat)
			Ushort.to_stream(stream, instance.ori_bone_count_repeat)
			Ushort.to_stream(stream, instance.scl_bone_count_repeat)
		Ushort.to_stream(stream, instance.zeros_1)
		if not (instance.context.version == 18):
			Uint.to_stream(stream, instance.zeros_1_new)
		Ushort.to_stream(stream, instance.float_count)
		Ubyte.to_stream(stream, instance.count_a)
		Ubyte.to_stream(stream, instance.count_b)
		Ushort.to_stream(stream, instance.target_bone_count)
		Ushort.to_stream(stream, instance.g)
		Array.to_stream(stream, instance.zeros_2, (57,), Uint, instance.context, 0, None)
		if instance.context.version == 18:
			Array.to_stream(stream, instance.extra_zeros_pc, (6,), Ushort, instance.context, 0, None)
		Ubyte.to_stream(stream, instance.pos_bone_min)
		Ubyte.to_stream(stream, instance.pos_bone_max)
		Ubyte.to_stream(stream, instance.ori_bone_min)
		Ubyte.to_stream(stream, instance.ori_bone_max)
		Byte.to_stream(stream, instance.scl_bone_min)
		Byte.to_stream(stream, instance.scl_bone_max)
		if not (instance.context.version == 18):
			Ubyte.to_stream(stream, instance.pos_bone_count_related)
			Ubyte.to_stream(stream, instance.pos_bone_count_repeat)
			Ubyte.to_stream(stream, instance.ori_bone_count_related)
			Ubyte.to_stream(stream, instance.ori_bone_count_repeat)
			Byte.to_stream(stream, instance.scl_bone_count_related)
			Byte.to_stream(stream, instance.scl_bone_count_repeat)
			Ushort.to_stream(stream, instance.zeros_end)
		Ushort.to_stream(stream, instance.zero_2_end)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'duration', Float, (0, None), (False, None)
		yield 'frame_count', Uint, (0, None), (False, None)
		yield 'b', Uint, (0, None), (False, None)
		yield 'zeros_0', Array, ((6,), Ushort, 0, None), (False, None)
		if instance.context.version == 18:
			yield 'extra_pc_1', Ushort, (0, None), (False, None)
		yield 'pos_bone_count', Ushort, (0, None), (False, None)
		yield 'ori_bone_count', Ushort, (0, None), (False, None)
		yield 'scl_bone_count', Ushort, (0, None), (False, None)
		if instance.context.version == 18:
			yield 'extra_pc', Uint64, (0, None), (False, None)
			yield 'pos_bone_count_repeat', Ushort, (0, None), (False, None)
			yield 'ori_bone_count_repeat', Ushort, (0, None), (False, None)
			yield 'scl_bone_count_repeat', Ushort, (0, None), (False, None)
		yield 'zeros_1', Ushort, (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'zeros_1_new', Uint, (0, None), (False, None)
		yield 'float_count', Ushort, (0, None), (False, None)
		yield 'count_a', Ubyte, (0, None), (False, None)
		yield 'count_b', Ubyte, (0, None), (False, None)
		yield 'target_bone_count', Ushort, (0, None), (False, None)
		yield 'g', Ushort, (0, None), (False, None)
		yield 'zeros_2', Array, ((57,), Uint, 0, None), (False, None)
		if instance.context.version == 18:
			yield 'extra_zeros_pc', Array, ((6,), Ushort, 0, None), (False, None)
		yield 'pos_bone_min', Ubyte, (0, None), (False, None)
		yield 'pos_bone_max', Ubyte, (0, None), (False, None)
		yield 'ori_bone_min', Ubyte, (0, None), (False, None)
		yield 'ori_bone_max', Ubyte, (0, None), (False, None)
		yield 'scl_bone_min', Byte, (0, None), (False, None)
		yield 'scl_bone_max', Byte, (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'pos_bone_count_related', Ubyte, (0, None), (False, None)
			yield 'pos_bone_count_repeat', Ubyte, (0, None), (False, None)
			yield 'ori_bone_count_related', Ubyte, (0, None), (False, None)
			yield 'ori_bone_count_repeat', Ubyte, (0, None), (False, None)
			yield 'scl_bone_count_related', Byte, (0, None), (False, None)
			yield 'scl_bone_count_repeat', Byte, (0, None), (False, None)
			yield 'zeros_end', Ushort, (0, None), (False, None)
		yield 'zero_2_end', Ushort, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ManiInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* duration = {self.fmt_member(self.duration, indent+1)}'
		s += f'\n	* frame_count = {self.fmt_member(self.frame_count, indent+1)}'
		s += f'\n	* b = {self.fmt_member(self.b, indent+1)}'
		s += f'\n	* zeros_0 = {self.fmt_member(self.zeros_0, indent+1)}'
		s += f'\n	* extra_pc_1 = {self.fmt_member(self.extra_pc_1, indent+1)}'
		s += f'\n	* pos_bone_count = {self.fmt_member(self.pos_bone_count, indent+1)}'
		s += f'\n	* ori_bone_count = {self.fmt_member(self.ori_bone_count, indent+1)}'
		s += f'\n	* scl_bone_count = {self.fmt_member(self.scl_bone_count, indent+1)}'
		s += f'\n	* extra_pc = {self.fmt_member(self.extra_pc, indent+1)}'
		s += f'\n	* pos_bone_count_repeat = {self.fmt_member(self.pos_bone_count_repeat, indent+1)}'
		s += f'\n	* ori_bone_count_repeat = {self.fmt_member(self.ori_bone_count_repeat, indent+1)}'
		s += f'\n	* scl_bone_count_repeat = {self.fmt_member(self.scl_bone_count_repeat, indent+1)}'
		s += f'\n	* zeros_1 = {self.fmt_member(self.zeros_1, indent+1)}'
		s += f'\n	* zeros_1_new = {self.fmt_member(self.zeros_1_new, indent+1)}'
		s += f'\n	* float_count = {self.fmt_member(self.float_count, indent+1)}'
		s += f'\n	* count_a = {self.fmt_member(self.count_a, indent+1)}'
		s += f'\n	* count_b = {self.fmt_member(self.count_b, indent+1)}'
		s += f'\n	* target_bone_count = {self.fmt_member(self.target_bone_count, indent+1)}'
		s += f'\n	* g = {self.fmt_member(self.g, indent+1)}'
		s += f'\n	* zeros_2 = {self.fmt_member(self.zeros_2, indent+1)}'
		s += f'\n	* extra_zeros_pc = {self.fmt_member(self.extra_zeros_pc, indent+1)}'
		s += f'\n	* pos_bone_min = {self.fmt_member(self.pos_bone_min, indent+1)}'
		s += f'\n	* pos_bone_max = {self.fmt_member(self.pos_bone_max, indent+1)}'
		s += f'\n	* ori_bone_min = {self.fmt_member(self.ori_bone_min, indent+1)}'
		s += f'\n	* ori_bone_max = {self.fmt_member(self.ori_bone_max, indent+1)}'
		s += f'\n	* scl_bone_min = {self.fmt_member(self.scl_bone_min, indent+1)}'
		s += f'\n	* scl_bone_max = {self.fmt_member(self.scl_bone_max, indent+1)}'
		s += f'\n	* pos_bone_count_related = {self.fmt_member(self.pos_bone_count_related, indent+1)}'
		s += f'\n	* pos_bone_count_repeat = {self.fmt_member(self.pos_bone_count_repeat, indent+1)}'
		s += f'\n	* ori_bone_count_related = {self.fmt_member(self.ori_bone_count_related, indent+1)}'
		s += f'\n	* ori_bone_count_repeat = {self.fmt_member(self.ori_bone_count_repeat, indent+1)}'
		s += f'\n	* scl_bone_count_related = {self.fmt_member(self.scl_bone_count_related, indent+1)}'
		s += f'\n	* scl_bone_count_repeat = {self.fmt_member(self.scl_bone_count_repeat, indent+1)}'
		s += f'\n	* zeros_end = {self.fmt_member(self.zeros_end, indent+1)}'
		s += f'\n	* zero_2_end = {self.fmt_member(self.zero_2_end, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
