from generated.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.compound.PadAlign import PadAlign
from generated.formats.manis.compound.Empty import Empty
from generated.formats.manis.compound.Repeat import Repeat
from generated.formats.ovl_base.compound.SmartPadding import SmartPadding
from generated.struct import StructBase


class ManiBlock(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.ref = 0
		self.pos_bones = 0
		self.ori_bones = 0
		self.scl_bones = 0
		self.floats = 0
		self.pos_bones_p = 0
		self.ori_bones_p = 0
		self.scl_bones_p = 0
		self.pos_bones_delta = 0
		self.ori_bones_delta = 0
		self.scl_bones_delta = 0

		# ?
		self.pad = 0

		# these are likely a scale reference or factor
		self.floatsa = 0

		# ?
		self.pad_2 = 0
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0

		# maybe
		self.scl_bone_count = 0

		# fixed
		self.zeros_18 = 0
		self.count = 0

		# usually 420, or 0
		self.quantisation_level = 0
		self.ref_2 = 0
		self.zeros = 0
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = 0

		# these are likely a scale reference or factor
		self.floatsb = 0

		# these are likely a scale reference or factor
		self.floats_second = 0

		# these are likely a scale reference or factor
		self.floats_third = 0

		# ?
		self.unk = 0

		# this seems to be vaguely related, but not always there?
		self.extra_pc_zero = 0
		self.repeats = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.ref = Empty(self.context, 0, None)
		if self.context.version == 18:
			self.pos_bones = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.pos_bones = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.ori_bones = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.ori_bones = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.scl_bones = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.scl_bones = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.floats = numpy.zeros((self.arg.float_count,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.floats = numpy.zeros((self.arg.float_count,), dtype=numpy.dtype('uint32'))
		self.pos_bones_p = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint8'))
		self.ori_bones_p = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint8'))
		self.scl_bones_p = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint8'))
		if self.arg.pos_bone_min >= 0:
			self.pos_bones_delta = numpy.zeros(((self.arg.pos_bone_max - self.arg.pos_bone_min) + 1,), dtype=numpy.dtype('uint8'))
		if self.arg.ori_bone_min >= 0:
			self.ori_bones_delta = numpy.zeros(((self.arg.ori_bone_max - self.arg.ori_bone_min) + 1,), dtype=numpy.dtype('uint8'))
		if self.arg.scl_bone_min >= 0:
			self.scl_bones_delta = numpy.zeros(((self.arg.scl_bone_max - self.arg.scl_bone_min) + 1,), dtype=numpy.dtype('uint8'))
		self.pad = PadAlign(self.context, 4, self.ref)
		self.floatsa = numpy.zeros((self.arg.frame_count, self.arg.float_count,), dtype=numpy.dtype('float32'))
		self.pad_2 = SmartPadding(self.context, 0, None)
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0
		self.scl_bone_count = 0
		self.zeros_18 = numpy.zeros((18,), dtype=numpy.dtype('uint32'))
		self.count = 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, 0, None)
		self.zeros = numpy.zeros((self.pos_bone_count,), dtype=numpy.dtype('uint8'))
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = PadAlign(self.context, 4, self.ref_2)
		self.floatsb = numpy.zeros((6,), dtype=numpy.dtype('float32'))
		self.floats_second = numpy.zeros((self.flag_1, 6,), dtype=numpy.dtype('float32'))
		if self.flag_2 > 1:
			self.floats_third = numpy.zeros((6,), dtype=numpy.dtype('float32'))
		self.unk = 0
		if self.context.version == 18:
			self.extra_pc_zero = 0
		self.repeats = Array((self.count,), Repeat, self.context, 0, None)

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
		instance.ref = Empty.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 18:
			instance.pos_bones = stream.read_ushorts((instance.arg.pos_bone_count,))
		if not (instance.context.version == 18):
			instance.pos_bones = stream.read_uints((instance.arg.pos_bone_count,))
		if instance.context.version == 18:
			instance.ori_bones = stream.read_ushorts((instance.arg.ori_bone_count,))
		if not (instance.context.version == 18):
			instance.ori_bones = stream.read_uints((instance.arg.ori_bone_count,))
		if instance.context.version == 18:
			instance.scl_bones = stream.read_ushorts((instance.arg.scl_bone_count,))
		if not (instance.context.version == 18):
			instance.scl_bones = stream.read_uints((instance.arg.scl_bone_count,))
		if instance.context.version == 18:
			instance.floats = stream.read_ushorts((instance.arg.float_count,))
		if not (instance.context.version == 18):
			instance.floats = stream.read_uints((instance.arg.float_count,))
		instance.pos_bones_p = stream.read_ubytes((instance.arg.pos_bone_count,))
		instance.ori_bones_p = stream.read_ubytes((instance.arg.ori_bone_count,))
		instance.scl_bones_p = stream.read_ubytes((instance.arg.scl_bone_count,))
		if instance.arg.pos_bone_min >= 0:
			instance.pos_bones_delta = stream.read_ubytes(((instance.arg.pos_bone_max - instance.arg.pos_bone_min) + 1,))
		if instance.arg.ori_bone_min >= 0:
			instance.ori_bones_delta = stream.read_ubytes(((instance.arg.ori_bone_max - instance.arg.ori_bone_min) + 1,))
		if instance.arg.scl_bone_min >= 0:
			instance.scl_bones_delta = stream.read_ubytes(((instance.arg.scl_bone_max - instance.arg.scl_bone_min) + 1,))
		instance.pad = PadAlign.from_stream(stream, instance.context, 4, instance.ref)
		instance.floatsa = stream.read_floats((instance.arg.frame_count, instance.arg.float_count,))
		instance.pad_2 = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.frame_count = stream.read_uint()
		instance.ori_bone_count = stream.read_uint()
		instance.pos_bone_count = stream.read_uint()
		instance.scl_bone_count = stream.read_uint()
		instance.zeros_18 = stream.read_uints((18,))
		instance.count = stream.read_ushort()
		instance.quantisation_level = stream.read_ushort()
		instance.ref_2 = Empty.from_stream(stream, instance.context, 0, None)
		instance.zeros = stream.read_ubytes((instance.pos_bone_count,))
		instance.flag_0 = stream.read_ubyte()
		instance.flag_1 = stream.read_ubyte()
		instance.flag_2 = stream.read_ubyte()
		instance.flag_3 = stream.read_ubyte()
		instance.anoth_pad = PadAlign.from_stream(stream, instance.context, 4, instance.ref_2)
		instance.floatsb = stream.read_floats((6,))
		instance.floats_second = stream.read_floats((instance.flag_1, 6,))
		if instance.flag_2 > 1:
			instance.floats_third = stream.read_floats((6,))
		instance.unk = stream.read_uint()
		if instance.context.version == 18:
			instance.extra_pc_zero = stream.read_uint64()
		instance.repeats = Array.from_stream(stream, (instance.count,), Repeat, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Empty.to_stream(stream, instance.ref)
		if instance.context.version == 18:
			stream.write_ushorts(instance.pos_bones)
		if not (instance.context.version == 18):
			stream.write_uints(instance.pos_bones)
		if instance.context.version == 18:
			stream.write_ushorts(instance.ori_bones)
		if not (instance.context.version == 18):
			stream.write_uints(instance.ori_bones)
		if instance.context.version == 18:
			stream.write_ushorts(instance.scl_bones)
		if not (instance.context.version == 18):
			stream.write_uints(instance.scl_bones)
		if instance.context.version == 18:
			stream.write_ushorts(instance.floats)
		if not (instance.context.version == 18):
			stream.write_uints(instance.floats)
		stream.write_ubytes(instance.pos_bones_p)
		stream.write_ubytes(instance.ori_bones_p)
		stream.write_ubytes(instance.scl_bones_p)
		if instance.arg.pos_bone_min >= 0:
			stream.write_ubytes(instance.pos_bones_delta)
		if instance.arg.ori_bone_min >= 0:
			stream.write_ubytes(instance.ori_bones_delta)
		if instance.arg.scl_bone_min >= 0:
			stream.write_ubytes(instance.scl_bones_delta)
		PadAlign.to_stream(stream, instance.pad)
		stream.write_floats(instance.floatsa)
		SmartPadding.to_stream(stream, instance.pad_2)
		stream.write_uint(instance.frame_count)
		stream.write_uint(instance.ori_bone_count)
		stream.write_uint(instance.pos_bone_count)
		stream.write_uint(instance.scl_bone_count)
		stream.write_uints(instance.zeros_18)
		stream.write_ushort(instance.count)
		stream.write_ushort(instance.quantisation_level)
		Empty.to_stream(stream, instance.ref_2)
		stream.write_ubytes(instance.zeros)
		stream.write_ubyte(instance.flag_0)
		stream.write_ubyte(instance.flag_1)
		stream.write_ubyte(instance.flag_2)
		stream.write_ubyte(instance.flag_3)
		PadAlign.to_stream(stream, instance.anoth_pad)
		stream.write_floats(instance.floatsb)
		stream.write_floats(instance.floats_second)
		if instance.flag_2 > 1:
			stream.write_floats(instance.floats_third)
		stream.write_uint(instance.unk)
		if instance.context.version == 18:
			stream.write_uint64(instance.extra_pc_zero)
		Array.to_stream(stream, instance.repeats, (instance.count,), Repeat, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('ref', Empty, (0, None))
		if instance.context.version == 18:
			yield ('pos_bones', Array, ((instance.arg.pos_bone_count,), Ushort, 0, None))
		if not (instance.context.version == 18):
			yield ('pos_bones', Array, ((instance.arg.pos_bone_count,), Uint, 0, None))
		if instance.context.version == 18:
			yield ('ori_bones', Array, ((instance.arg.ori_bone_count,), Ushort, 0, None))
		if not (instance.context.version == 18):
			yield ('ori_bones', Array, ((instance.arg.ori_bone_count,), Uint, 0, None))
		if instance.context.version == 18:
			yield ('scl_bones', Array, ((instance.arg.scl_bone_count,), Ushort, 0, None))
		if not (instance.context.version == 18):
			yield ('scl_bones', Array, ((instance.arg.scl_bone_count,), Uint, 0, None))
		if instance.context.version == 18:
			yield ('floats', Array, ((instance.arg.float_count,), Ushort, 0, None))
		if not (instance.context.version == 18):
			yield ('floats', Array, ((instance.arg.float_count,), Uint, 0, None))
		yield ('pos_bones_p', Array, ((instance.arg.pos_bone_count,), Ubyte, 0, None))
		yield ('ori_bones_p', Array, ((instance.arg.ori_bone_count,), Ubyte, 0, None))
		yield ('scl_bones_p', Array, ((instance.arg.scl_bone_count,), Ubyte, 0, None))
		if instance.arg.pos_bone_min >= 0:
			yield ('pos_bones_delta', Array, (((instance.arg.pos_bone_max - instance.arg.pos_bone_min) + 1,), Ubyte, 0, None))
		if instance.arg.ori_bone_min >= 0:
			yield ('ori_bones_delta', Array, (((instance.arg.ori_bone_max - instance.arg.ori_bone_min) + 1,), Ubyte, 0, None))
		if instance.arg.scl_bone_min >= 0:
			yield ('scl_bones_delta', Array, (((instance.arg.scl_bone_max - instance.arg.scl_bone_min) + 1,), Ubyte, 0, None))
		yield ('pad', PadAlign, (4, instance.ref))
		yield ('floatsa', Array, ((instance.arg.frame_count, instance.arg.float_count,), Float, 0, None))
		yield ('pad_2', SmartPadding, (0, None))
		yield ('frame_count', Uint, (0, None))
		yield ('ori_bone_count', Uint, (0, None))
		yield ('pos_bone_count', Uint, (0, None))
		yield ('scl_bone_count', Uint, (0, None))
		yield ('zeros_18', Array, ((18,), Uint, 0, None))
		yield ('count', Ushort, (0, None))
		yield ('quantisation_level', Ushort, (0, None))
		yield ('ref_2', Empty, (0, None))
		yield ('zeros', Array, ((instance.pos_bone_count,), Ubyte, 0, None))
		yield ('flag_0', Ubyte, (0, None))
		yield ('flag_1', Ubyte, (0, None))
		yield ('flag_2', Ubyte, (0, None))
		yield ('flag_3', Ubyte, (0, None))
		yield ('anoth_pad', PadAlign, (4, instance.ref_2))
		yield ('floatsb', Array, ((6,), Float, 0, None))
		yield ('floats_second', Array, ((instance.flag_1, 6,), Float, 0, None))
		if instance.flag_2 > 1:
			yield ('floats_third', Array, ((6,), Float, 0, None))
		yield ('unk', Uint, (0, None))
		if instance.context.version == 18:
			yield ('extra_pc_zero', Uint64, (0, None))
		yield ('repeats', Array, ((instance.count,), Repeat, 0, None))

	def get_info_str(self, indent=0):
		return f'ManiBlock [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ref = {fmt_member(self.ref, indent+1)}'
		s += f'\n	* pos_bones = {fmt_member(self.pos_bones, indent+1)}'
		s += f'\n	* ori_bones = {fmt_member(self.ori_bones, indent+1)}'
		s += f'\n	* scl_bones = {fmt_member(self.scl_bones, indent+1)}'
		s += f'\n	* floats = {fmt_member(self.floats, indent+1)}'
		s += f'\n	* pos_bones_p = {fmt_member(self.pos_bones_p, indent+1)}'
		s += f'\n	* ori_bones_p = {fmt_member(self.ori_bones_p, indent+1)}'
		s += f'\n	* scl_bones_p = {fmt_member(self.scl_bones_p, indent+1)}'
		s += f'\n	* pos_bones_delta = {fmt_member(self.pos_bones_delta, indent+1)}'
		s += f'\n	* ori_bones_delta = {fmt_member(self.ori_bones_delta, indent+1)}'
		s += f'\n	* scl_bones_delta = {fmt_member(self.scl_bones_delta, indent+1)}'
		s += f'\n	* pad = {fmt_member(self.pad, indent+1)}'
		s += f'\n	* floatsa = {fmt_member(self.floatsa, indent+1)}'
		s += f'\n	* pad_2 = {fmt_member(self.pad_2, indent+1)}'
		s += f'\n	* frame_count = {fmt_member(self.frame_count, indent+1)}'
		s += f'\n	* ori_bone_count = {fmt_member(self.ori_bone_count, indent+1)}'
		s += f'\n	* pos_bone_count = {fmt_member(self.pos_bone_count, indent+1)}'
		s += f'\n	* scl_bone_count = {fmt_member(self.scl_bone_count, indent+1)}'
		s += f'\n	* zeros_18 = {fmt_member(self.zeros_18, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		s += f'\n	* quantisation_level = {fmt_member(self.quantisation_level, indent+1)}'
		s += f'\n	* ref_2 = {fmt_member(self.ref_2, indent+1)}'
		s += f'\n	* zeros = {fmt_member(self.zeros, indent+1)}'
		s += f'\n	* flag_0 = {fmt_member(self.flag_0, indent+1)}'
		s += f'\n	* flag_1 = {fmt_member(self.flag_1, indent+1)}'
		s += f'\n	* flag_2 = {fmt_member(self.flag_2, indent+1)}'
		s += f'\n	* flag_3 = {fmt_member(self.flag_3, indent+1)}'
		s += f'\n	* anoth_pad = {fmt_member(self.anoth_pad, indent+1)}'
		s += f'\n	* floatsb = {fmt_member(self.floatsb, indent+1)}'
		s += f'\n	* floats_second = {fmt_member(self.floats_second, indent+1)}'
		s += f'\n	* floats_third = {fmt_member(self.floats_third, indent+1)}'
		s += f'\n	* unk = {fmt_member(self.unk, indent+1)}'
		s += f'\n	* extra_pc_zero = {fmt_member(self.extra_pc_zero, indent+1)}'
		s += f'\n	* repeats = {fmt_member(self.repeats, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
