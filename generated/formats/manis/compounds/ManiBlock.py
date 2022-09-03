import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.manis.compounds.Empty import Empty
from generated.formats.manis.compounds.Repeat import Repeat
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class ManiBlock(BaseStruct):

	__name__ = 'ManiBlock'

	_import_path = 'generated.formats.manis.compounds.ManiBlock'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = Empty(self.context, 0, None)
		self.pos_bones = Array((0,), Uint, self.context, 0, None)
		self.ori_bones = Array((0,), Uint, self.context, 0, None)
		self.scl_bones = Array((0,), Uint, self.context, 0, None)
		self.floats = Array((0,), Uint, self.context, 0, None)
		self.pos_bones_p = Array((0,), Ubyte, self.context, 0, None)
		self.ori_bones_p = Array((0,), Ubyte, self.context, 0, None)
		self.scl_bones_p = Array((0,), Ubyte, self.context, 0, None)
		self.pos_bones_delta = Array((0,), Ubyte, self.context, 0, None)
		self.ori_bones_delta = Array((0,), Ubyte, self.context, 0, None)
		self.scl_bones_delta = Array((0,), Ubyte, self.context, 0, None)

		# ?
		self.pad = PadAlign(self.context, 4, self.ref)

		# these are likely a scale reference or factor
		self.floatsa = Array((0,), Float, self.context, 0, None)

		# ?
		self.pad_2 = SmartPadding(self.context, 0, None)
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0

		# maybe
		self.scl_bone_count = 0

		# fixed
		self.zeros_18 = Array((0,), Uint, self.context, 0, None)
		self.count = 0

		# usually 420, or 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, 0, None)
		self.some_indices = Array((0,), Ubyte, self.context, 0, None)
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = PadAlign(self.context, 4, self.ref_2)

		# these are likely a scale reference or factor
		self.floatsb = Array((0,), Float, self.context, 0, None)

		# these are likely a scale reference or factor
		self.floats_second = Array((0,), Float, self.context, 0, None)

		# these are likely a scale reference or factor
		self.floats_third = Array((0,), Float, self.context, 0, None)

		# present in feeder, not in dino
		self.unk = 0

		# this seems to be vaguely related, but not always there?
		self.extra_pc_zero = 0
		self.repeats = Array((0,), Repeat, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ref = Empty(self.context, 0, None)
		if self.context.version <= 257:
			self.pos_bones = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint16'))
		if self.context.version >= 258:
			self.pos_bones = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint32'))
		if self.context.version <= 257:
			self.ori_bones = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint16'))
		if self.context.version >= 258:
			self.ori_bones = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint32'))
		if self.context.version <= 257:
			self.scl_bones = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint16'))
		if self.context.version >= 258:
			self.scl_bones = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint32'))
		if self.context.version <= 257:
			self.floats = numpy.zeros((self.arg.float_count,), dtype=numpy.dtype('uint16'))
		if self.context.version >= 258:
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
		self.some_indices = numpy.zeros((self.pos_bone_count,), dtype=numpy.dtype('uint8'))
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = PadAlign(self.context, 4, self.ref_2)
		self.floatsb = numpy.zeros((6,), dtype=numpy.dtype('float32'))
		self.floats_second = numpy.zeros((self.flag_1, 6,), dtype=numpy.dtype('float32'))
		if self.flag_2 > 1:
			self.floats_third = numpy.zeros((6,), dtype=numpy.dtype('float32'))
		if self.arg.count_a == 255:
			self.unk = 0
		if self.context.version <= 257:
			self.extra_pc_zero = 0
		self.repeats = Array((self.count,), Repeat, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ref = Empty.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 257:
			instance.pos_bones = Array.from_stream(stream, instance.context, 0, None, (instance.arg.pos_bone_count,), Ushort)
		if instance.context.version >= 258:
			instance.pos_bones = Array.from_stream(stream, instance.context, 0, None, (instance.arg.pos_bone_count,), Uint)
		if instance.context.version <= 257:
			instance.ori_bones = Array.from_stream(stream, instance.context, 0, None, (instance.arg.ori_bone_count,), Ushort)
		if instance.context.version >= 258:
			instance.ori_bones = Array.from_stream(stream, instance.context, 0, None, (instance.arg.ori_bone_count,), Uint)
		if instance.context.version <= 257:
			instance.scl_bones = Array.from_stream(stream, instance.context, 0, None, (instance.arg.scl_bone_count,), Ushort)
		if instance.context.version >= 258:
			instance.scl_bones = Array.from_stream(stream, instance.context, 0, None, (instance.arg.scl_bone_count,), Uint)
		if instance.context.version <= 257:
			instance.floats = Array.from_stream(stream, instance.context, 0, None, (instance.arg.float_count,), Ushort)
		if instance.context.version >= 258:
			instance.floats = Array.from_stream(stream, instance.context, 0, None, (instance.arg.float_count,), Uint)
		instance.pos_bones_p = Array.from_stream(stream, instance.context, 0, None, (instance.arg.pos_bone_count,), Ubyte)
		instance.ori_bones_p = Array.from_stream(stream, instance.context, 0, None, (instance.arg.ori_bone_count,), Ubyte)
		instance.scl_bones_p = Array.from_stream(stream, instance.context, 0, None, (instance.arg.scl_bone_count,), Ubyte)
		if instance.arg.pos_bone_min >= 0:
			instance.pos_bones_delta = Array.from_stream(stream, instance.context, 0, None, ((instance.arg.pos_bone_max - instance.arg.pos_bone_min) + 1,), Ubyte)
		if instance.arg.ori_bone_min >= 0:
			instance.ori_bones_delta = Array.from_stream(stream, instance.context, 0, None, ((instance.arg.ori_bone_max - instance.arg.ori_bone_min) + 1,), Ubyte)
		if instance.arg.scl_bone_min >= 0:
			instance.scl_bones_delta = Array.from_stream(stream, instance.context, 0, None, ((instance.arg.scl_bone_max - instance.arg.scl_bone_min) + 1,), Ubyte)
		instance.pad = PadAlign.from_stream(stream, instance.context, 4, instance.ref)
		instance.floatsa = Array.from_stream(stream, instance.context, 0, None, (instance.arg.frame_count, instance.arg.float_count,), Float)
		instance.pad_2 = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.frame_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.ori_bone_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.pos_bone_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.scl_bone_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros_18 = Array.from_stream(stream, instance.context, 0, None, (18,), Uint)
		instance.count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.quantisation_level = Ushort.from_stream(stream, instance.context, 0, None)
		instance.ref_2 = Empty.from_stream(stream, instance.context, 0, None)
		instance.some_indices = Array.from_stream(stream, instance.context, 0, None, (instance.pos_bone_count,), Ubyte)
		instance.flag_0 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.flag_1 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.flag_2 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.flag_3 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.anoth_pad = PadAlign.from_stream(stream, instance.context, 4, instance.ref_2)
		instance.floatsb = Array.from_stream(stream, instance.context, 0, None, (6,), Float)
		instance.floats_second = Array.from_stream(stream, instance.context, 0, None, (instance.flag_1, 6,), Float)
		if instance.flag_2 > 1:
			instance.floats_third = Array.from_stream(stream, instance.context, 0, None, (6,), Float)
		if instance.arg.count_a == 255:
			instance.unk = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 257:
			instance.extra_pc_zero = Uint64.from_stream(stream, instance.context, 0, None)
		instance.repeats = Array.from_stream(stream, instance.context, 0, None, (instance.count,), Repeat)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Empty.to_stream(stream, instance.ref)
		if instance.context.version <= 257:
			Array.to_stream(stream, instance.pos_bones, (instance.arg.pos_bone_count,), Ushort, instance.context, 0, None)
		if instance.context.version >= 258:
			Array.to_stream(stream, instance.pos_bones, (instance.arg.pos_bone_count,), Uint, instance.context, 0, None)
		if instance.context.version <= 257:
			Array.to_stream(stream, instance.ori_bones, (instance.arg.ori_bone_count,), Ushort, instance.context, 0, None)
		if instance.context.version >= 258:
			Array.to_stream(stream, instance.ori_bones, (instance.arg.ori_bone_count,), Uint, instance.context, 0, None)
		if instance.context.version <= 257:
			Array.to_stream(stream, instance.scl_bones, (instance.arg.scl_bone_count,), Ushort, instance.context, 0, None)
		if instance.context.version >= 258:
			Array.to_stream(stream, instance.scl_bones, (instance.arg.scl_bone_count,), Uint, instance.context, 0, None)
		if instance.context.version <= 257:
			Array.to_stream(stream, instance.floats, (instance.arg.float_count,), Ushort, instance.context, 0, None)
		if instance.context.version >= 258:
			Array.to_stream(stream, instance.floats, (instance.arg.float_count,), Uint, instance.context, 0, None)
		Array.to_stream(stream, instance.pos_bones_p, (instance.arg.pos_bone_count,), Ubyte, instance.context, 0, None)
		Array.to_stream(stream, instance.ori_bones_p, (instance.arg.ori_bone_count,), Ubyte, instance.context, 0, None)
		Array.to_stream(stream, instance.scl_bones_p, (instance.arg.scl_bone_count,), Ubyte, instance.context, 0, None)
		if instance.arg.pos_bone_min >= 0:
			Array.to_stream(stream, instance.pos_bones_delta, ((instance.arg.pos_bone_max - instance.arg.pos_bone_min) + 1,), Ubyte, instance.context, 0, None)
		if instance.arg.ori_bone_min >= 0:
			Array.to_stream(stream, instance.ori_bones_delta, ((instance.arg.ori_bone_max - instance.arg.ori_bone_min) + 1,), Ubyte, instance.context, 0, None)
		if instance.arg.scl_bone_min >= 0:
			Array.to_stream(stream, instance.scl_bones_delta, ((instance.arg.scl_bone_max - instance.arg.scl_bone_min) + 1,), Ubyte, instance.context, 0, None)
		PadAlign.to_stream(stream, instance.pad)
		Array.to_stream(stream, instance.floatsa, (instance.arg.frame_count, instance.arg.float_count,), Float, instance.context, 0, None)
		SmartPadding.to_stream(stream, instance.pad_2)
		Uint.to_stream(stream, instance.frame_count)
		Uint.to_stream(stream, instance.ori_bone_count)
		Uint.to_stream(stream, instance.pos_bone_count)
		Uint.to_stream(stream, instance.scl_bone_count)
		Array.to_stream(stream, instance.zeros_18, (18,), Uint, instance.context, 0, None)
		Ushort.to_stream(stream, instance.count)
		Ushort.to_stream(stream, instance.quantisation_level)
		Empty.to_stream(stream, instance.ref_2)
		Array.to_stream(stream, instance.some_indices, (instance.pos_bone_count,), Ubyte, instance.context, 0, None)
		Ubyte.to_stream(stream, instance.flag_0)
		Ubyte.to_stream(stream, instance.flag_1)
		Ubyte.to_stream(stream, instance.flag_2)
		Ubyte.to_stream(stream, instance.flag_3)
		PadAlign.to_stream(stream, instance.anoth_pad)
		Array.to_stream(stream, instance.floatsb, (6,), Float, instance.context, 0, None)
		Array.to_stream(stream, instance.floats_second, (instance.flag_1, 6,), Float, instance.context, 0, None)
		if instance.flag_2 > 1:
			Array.to_stream(stream, instance.floats_third, (6,), Float, instance.context, 0, None)
		if instance.arg.count_a == 255:
			Uint.to_stream(stream, instance.unk)
		if instance.context.version <= 257:
			Uint64.to_stream(stream, instance.extra_pc_zero)
		Array.to_stream(stream, instance.repeats, (instance.count,), Repeat, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ref', Empty, (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'pos_bones', Array, (0, None, (instance.arg.pos_bone_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'pos_bones', Array, (0, None, (instance.arg.pos_bone_count,), Uint), (False, None)
		if instance.context.version <= 257:
			yield 'ori_bones', Array, (0, None, (instance.arg.ori_bone_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'ori_bones', Array, (0, None, (instance.arg.ori_bone_count,), Uint), (False, None)
		if instance.context.version <= 257:
			yield 'scl_bones', Array, (0, None, (instance.arg.scl_bone_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'scl_bones', Array, (0, None, (instance.arg.scl_bone_count,), Uint), (False, None)
		if instance.context.version <= 257:
			yield 'floats', Array, (0, None, (instance.arg.float_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'floats', Array, (0, None, (instance.arg.float_count,), Uint), (False, None)
		yield 'pos_bones_p', Array, (0, None, (instance.arg.pos_bone_count,), Ubyte), (False, None)
		yield 'ori_bones_p', Array, (0, None, (instance.arg.ori_bone_count,), Ubyte), (False, None)
		yield 'scl_bones_p', Array, (0, None, (instance.arg.scl_bone_count,), Ubyte), (False, None)
		if instance.arg.pos_bone_min >= 0:
			yield 'pos_bones_delta', Array, (0, None, ((instance.arg.pos_bone_max - instance.arg.pos_bone_min) + 1,), Ubyte), (False, None)
		if instance.arg.ori_bone_min >= 0:
			yield 'ori_bones_delta', Array, (0, None, ((instance.arg.ori_bone_max - instance.arg.ori_bone_min) + 1,), Ubyte), (False, None)
		if instance.arg.scl_bone_min >= 0:
			yield 'scl_bones_delta', Array, (0, None, ((instance.arg.scl_bone_max - instance.arg.scl_bone_min) + 1,), Ubyte), (False, None)
		yield 'pad', PadAlign, (4, instance.ref), (False, None)
		yield 'floatsa', Array, (0, None, (instance.arg.frame_count, instance.arg.float_count,), Float), (False, None)
		yield 'pad_2', SmartPadding, (0, None), (False, None)
		yield 'frame_count', Uint, (0, None), (False, None)
		yield 'ori_bone_count', Uint, (0, None), (False, None)
		yield 'pos_bone_count', Uint, (0, None), (False, None)
		yield 'scl_bone_count', Uint, (0, None), (False, None)
		yield 'zeros_18', Array, (0, None, (18,), Uint), (False, None)
		yield 'count', Ushort, (0, None), (False, None)
		yield 'quantisation_level', Ushort, (0, None), (False, None)
		yield 'ref_2', Empty, (0, None), (False, None)
		yield 'some_indices', Array, (0, None, (instance.pos_bone_count,), Ubyte), (False, None)
		yield 'flag_0', Ubyte, (0, None), (False, None)
		yield 'flag_1', Ubyte, (0, None), (False, None)
		yield 'flag_2', Ubyte, (0, None), (False, None)
		yield 'flag_3', Ubyte, (0, None), (False, None)
		yield 'anoth_pad', PadAlign, (4, instance.ref_2), (False, None)
		yield 'floatsb', Array, (0, None, (6,), Float), (False, None)
		yield 'floats_second', Array, (0, None, (instance.flag_1, 6,), Float), (False, None)
		if instance.flag_2 > 1:
			yield 'floats_third', Array, (0, None, (6,), Float), (False, None)
		if instance.arg.count_a == 255:
			yield 'unk', Uint, (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'extra_pc_zero', Uint64, (0, None), (False, None)
		yield 'repeats', Array, (0, None, (instance.count,), Repeat), (False, None)

	def get_info_str(self, indent=0):
		return f'ManiBlock [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ref = {self.fmt_member(self.ref, indent+1)}'
		s += f'\n	* pos_bones = {self.fmt_member(self.pos_bones, indent+1)}'
		s += f'\n	* ori_bones = {self.fmt_member(self.ori_bones, indent+1)}'
		s += f'\n	* scl_bones = {self.fmt_member(self.scl_bones, indent+1)}'
		s += f'\n	* floats = {self.fmt_member(self.floats, indent+1)}'
		s += f'\n	* pos_bones_p = {self.fmt_member(self.pos_bones_p, indent+1)}'
		s += f'\n	* ori_bones_p = {self.fmt_member(self.ori_bones_p, indent+1)}'
		s += f'\n	* scl_bones_p = {self.fmt_member(self.scl_bones_p, indent+1)}'
		s += f'\n	* pos_bones_delta = {self.fmt_member(self.pos_bones_delta, indent+1)}'
		s += f'\n	* ori_bones_delta = {self.fmt_member(self.ori_bones_delta, indent+1)}'
		s += f'\n	* scl_bones_delta = {self.fmt_member(self.scl_bones_delta, indent+1)}'
		s += f'\n	* pad = {self.fmt_member(self.pad, indent+1)}'
		s += f'\n	* floatsa = {self.fmt_member(self.floatsa, indent+1)}'
		s += f'\n	* pad_2 = {self.fmt_member(self.pad_2, indent+1)}'
		s += f'\n	* frame_count = {self.fmt_member(self.frame_count, indent+1)}'
		s += f'\n	* ori_bone_count = {self.fmt_member(self.ori_bone_count, indent+1)}'
		s += f'\n	* pos_bone_count = {self.fmt_member(self.pos_bone_count, indent+1)}'
		s += f'\n	* scl_bone_count = {self.fmt_member(self.scl_bone_count, indent+1)}'
		s += f'\n	* zeros_18 = {self.fmt_member(self.zeros_18, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* quantisation_level = {self.fmt_member(self.quantisation_level, indent+1)}'
		s += f'\n	* ref_2 = {self.fmt_member(self.ref_2, indent+1)}'
		s += f'\n	* some_indices = {self.fmt_member(self.some_indices, indent+1)}'
		s += f'\n	* flag_0 = {self.fmt_member(self.flag_0, indent+1)}'
		s += f'\n	* flag_1 = {self.fmt_member(self.flag_1, indent+1)}'
		s += f'\n	* flag_2 = {self.fmt_member(self.flag_2, indent+1)}'
		s += f'\n	* flag_3 = {self.fmt_member(self.flag_3, indent+1)}'
		s += f'\n	* anoth_pad = {self.fmt_member(self.anoth_pad, indent+1)}'
		s += f'\n	* floatsb = {self.fmt_member(self.floatsb, indent+1)}'
		s += f'\n	* floats_second = {self.fmt_member(self.floats_second, indent+1)}'
		s += f'\n	* floats_third = {self.fmt_member(self.floats_third, indent+1)}'
		s += f'\n	* unk = {self.fmt_member(self.unk, indent+1)}'
		s += f'\n	* extra_pc_zero = {self.fmt_member(self.extra_pc_zero, indent+1)}'
		s += f'\n	* repeats = {self.fmt_member(self.repeats, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
