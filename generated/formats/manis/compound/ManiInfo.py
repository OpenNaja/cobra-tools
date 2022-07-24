from generated.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.struct import StructBase


class ManiInfo(StructBase):

	"""
	288 bytes for JWE / PZ
	304 bytes for PC
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.duration = 0
		self.frame_count = 0

		# ?
		self.b = 0
		self.zeros_0 = 0
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
		self.zeros_2 = 0

		# rest 14 bytes
		self.extra_zeros_pc = 0
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
		instance.duration = stream.read_float()
		instance.frame_count = stream.read_uint()
		instance.b = stream.read_uint()
		instance.zeros_0 = stream.read_ushorts((6,))
		if instance.context.version == 18:
			instance.extra_pc_1 = stream.read_ushort()
		instance.pos_bone_count = stream.read_ushort()
		instance.ori_bone_count = stream.read_ushort()
		instance.scl_bone_count = stream.read_ushort()
		if instance.context.version == 18:
			instance.extra_pc = stream.read_uint64()
			instance.pos_bone_count_repeat = stream.read_ushort()
			instance.ori_bone_count_repeat = stream.read_ushort()
			instance.scl_bone_count_repeat = stream.read_ushort()
		instance.zeros_1 = stream.read_ushort()
		if not (instance.context.version == 18):
			instance.zeros_1_new = stream.read_uint()
		instance.float_count = stream.read_ushort()
		instance.count_a = stream.read_ubyte()
		instance.count_b = stream.read_ubyte()
		instance.target_bone_count = stream.read_ushort()
		instance.g = stream.read_ushort()
		instance.zeros_2 = stream.read_uints((57,))
		if instance.context.version == 18:
			instance.extra_zeros_pc = stream.read_ushorts((6,))
		instance.pos_bone_min = stream.read_ubyte()
		instance.pos_bone_max = stream.read_ubyte()
		instance.ori_bone_min = stream.read_ubyte()
		instance.ori_bone_max = stream.read_ubyte()
		instance.scl_bone_min = stream.read_byte()
		instance.scl_bone_max = stream.read_byte()
		if not (instance.context.version == 18):
			instance.pos_bone_count_related = stream.read_ubyte()
			instance.pos_bone_count_repeat = stream.read_ubyte()
			instance.ori_bone_count_related = stream.read_ubyte()
			instance.ori_bone_count_repeat = stream.read_ubyte()
			instance.scl_bone_count_related = stream.read_byte()
			instance.scl_bone_count_repeat = stream.read_byte()
			instance.zeros_end = stream.read_ushort()
		instance.zero_2_end = stream.read_ushort()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.duration)
		stream.write_uint(instance.frame_count)
		stream.write_uint(instance.b)
		stream.write_ushorts(instance.zeros_0)
		if instance.context.version == 18:
			stream.write_ushort(instance.extra_pc_1)
		stream.write_ushort(instance.pos_bone_count)
		stream.write_ushort(instance.ori_bone_count)
		stream.write_ushort(instance.scl_bone_count)
		if instance.context.version == 18:
			stream.write_uint64(instance.extra_pc)
			stream.write_ushort(instance.pos_bone_count_repeat)
			stream.write_ushort(instance.ori_bone_count_repeat)
			stream.write_ushort(instance.scl_bone_count_repeat)
		stream.write_ushort(instance.zeros_1)
		if not (instance.context.version == 18):
			stream.write_uint(instance.zeros_1_new)
		stream.write_ushort(instance.float_count)
		stream.write_ubyte(instance.count_a)
		stream.write_ubyte(instance.count_b)
		stream.write_ushort(instance.target_bone_count)
		stream.write_ushort(instance.g)
		stream.write_uints(instance.zeros_2)
		if instance.context.version == 18:
			stream.write_ushorts(instance.extra_zeros_pc)
		stream.write_ubyte(instance.pos_bone_min)
		stream.write_ubyte(instance.pos_bone_max)
		stream.write_ubyte(instance.ori_bone_min)
		stream.write_ubyte(instance.ori_bone_max)
		stream.write_byte(instance.scl_bone_min)
		stream.write_byte(instance.scl_bone_max)
		if not (instance.context.version == 18):
			stream.write_ubyte(instance.pos_bone_count_related)
			stream.write_ubyte(instance.pos_bone_count_repeat)
			stream.write_ubyte(instance.ori_bone_count_related)
			stream.write_ubyte(instance.ori_bone_count_repeat)
			stream.write_byte(instance.scl_bone_count_related)
			stream.write_byte(instance.scl_bone_count_repeat)
			stream.write_ushort(instance.zeros_end)
		stream.write_ushort(instance.zero_2_end)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('duration', Float, (0, None))
		yield ('frame_count', Uint, (0, None))
		yield ('b', Uint, (0, None))
		yield ('zeros_0', Array, ((6,), Ushort, 0, None))
		if instance.context.version == 18:
			yield ('extra_pc_1', Ushort, (0, None))
		yield ('pos_bone_count', Ushort, (0, None))
		yield ('ori_bone_count', Ushort, (0, None))
		yield ('scl_bone_count', Ushort, (0, None))
		if instance.context.version == 18:
			yield ('extra_pc', Uint64, (0, None))
			yield ('pos_bone_count_repeat', Ushort, (0, None))
			yield ('ori_bone_count_repeat', Ushort, (0, None))
			yield ('scl_bone_count_repeat', Ushort, (0, None))
		yield ('zeros_1', Ushort, (0, None))
		if not (instance.context.version == 18):
			yield ('zeros_1_new', Uint, (0, None))
		yield ('float_count', Ushort, (0, None))
		yield ('count_a', Ubyte, (0, None))
		yield ('count_b', Ubyte, (0, None))
		yield ('target_bone_count', Ushort, (0, None))
		yield ('g', Ushort, (0, None))
		yield ('zeros_2', Array, ((57,), Uint, 0, None))
		if instance.context.version == 18:
			yield ('extra_zeros_pc', Array, ((6,), Ushort, 0, None))
		yield ('pos_bone_min', Ubyte, (0, None))
		yield ('pos_bone_max', Ubyte, (0, None))
		yield ('ori_bone_min', Ubyte, (0, None))
		yield ('ori_bone_max', Ubyte, (0, None))
		yield ('scl_bone_min', Byte, (0, None))
		yield ('scl_bone_max', Byte, (0, None))
		if not (instance.context.version == 18):
			yield ('pos_bone_count_related', Ubyte, (0, None))
			yield ('pos_bone_count_repeat', Ubyte, (0, None))
			yield ('ori_bone_count_related', Ubyte, (0, None))
			yield ('ori_bone_count_repeat', Ubyte, (0, None))
			yield ('scl_bone_count_related', Byte, (0, None))
			yield ('scl_bone_count_repeat', Byte, (0, None))
			yield ('zeros_end', Ushort, (0, None))
		yield ('zero_2_end', Ushort, (0, None))

	def get_info_str(self, indent=0):
		return f'ManiInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* duration = {fmt_member(self.duration, indent+1)}'
		s += f'\n	* frame_count = {fmt_member(self.frame_count, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* zeros_0 = {fmt_member(self.zeros_0, indent+1)}'
		s += f'\n	* extra_pc_1 = {fmt_member(self.extra_pc_1, indent+1)}'
		s += f'\n	* pos_bone_count = {fmt_member(self.pos_bone_count, indent+1)}'
		s += f'\n	* ori_bone_count = {fmt_member(self.ori_bone_count, indent+1)}'
		s += f'\n	* scl_bone_count = {fmt_member(self.scl_bone_count, indent+1)}'
		s += f'\n	* extra_pc = {fmt_member(self.extra_pc, indent+1)}'
		s += f'\n	* pos_bone_count_repeat = {fmt_member(self.pos_bone_count_repeat, indent+1)}'
		s += f'\n	* ori_bone_count_repeat = {fmt_member(self.ori_bone_count_repeat, indent+1)}'
		s += f'\n	* scl_bone_count_repeat = {fmt_member(self.scl_bone_count_repeat, indent+1)}'
		s += f'\n	* zeros_1 = {fmt_member(self.zeros_1, indent+1)}'
		s += f'\n	* zeros_1_new = {fmt_member(self.zeros_1_new, indent+1)}'
		s += f'\n	* float_count = {fmt_member(self.float_count, indent+1)}'
		s += f'\n	* count_a = {fmt_member(self.count_a, indent+1)}'
		s += f'\n	* count_b = {fmt_member(self.count_b, indent+1)}'
		s += f'\n	* target_bone_count = {fmt_member(self.target_bone_count, indent+1)}'
		s += f'\n	* g = {fmt_member(self.g, indent+1)}'
		s += f'\n	* zeros_2 = {fmt_member(self.zeros_2, indent+1)}'
		s += f'\n	* extra_zeros_pc = {fmt_member(self.extra_zeros_pc, indent+1)}'
		s += f'\n	* pos_bone_min = {fmt_member(self.pos_bone_min, indent+1)}'
		s += f'\n	* pos_bone_max = {fmt_member(self.pos_bone_max, indent+1)}'
		s += f'\n	* ori_bone_min = {fmt_member(self.ori_bone_min, indent+1)}'
		s += f'\n	* ori_bone_max = {fmt_member(self.ori_bone_max, indent+1)}'
		s += f'\n	* scl_bone_min = {fmt_member(self.scl_bone_min, indent+1)}'
		s += f'\n	* scl_bone_max = {fmt_member(self.scl_bone_max, indent+1)}'
		s += f'\n	* pos_bone_count_related = {fmt_member(self.pos_bone_count_related, indent+1)}'
		s += f'\n	* pos_bone_count_repeat = {fmt_member(self.pos_bone_count_repeat, indent+1)}'
		s += f'\n	* ori_bone_count_related = {fmt_member(self.ori_bone_count_related, indent+1)}'
		s += f'\n	* ori_bone_count_repeat = {fmt_member(self.ori_bone_count_repeat, indent+1)}'
		s += f'\n	* scl_bone_count_related = {fmt_member(self.scl_bone_count_related, indent+1)}'
		s += f'\n	* scl_bone_count_repeat = {fmt_member(self.scl_bone_count_repeat, indent+1)}'
		s += f'\n	* zeros_end = {fmt_member(self.zeros_end, indent+1)}'
		s += f'\n	* zero_2_end = {fmt_member(self.zero_2_end, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
