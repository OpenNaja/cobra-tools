import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.manis.compound.Empty import Empty
from generated.formats.manis.compound.PadAlign import PadAlign
from generated.formats.manis.compound.Repeat import Repeat
from generated.formats.manis.compound.SmartPadding import SmartPadding


class ManiBlock:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ref = Empty(self.context, None, None)
		self.pos_bones = numpy.zeros((), dtype='ushort')
		self.pos_bones = numpy.zeros((), dtype='uint')
		self.ori_bones = numpy.zeros((), dtype='ushort')
		self.ori_bones = numpy.zeros((), dtype='uint')
		self.scl_bones = numpy.zeros((), dtype='ushort')
		self.scl_bones = numpy.zeros((), dtype='uint')
		self.floats = numpy.zeros((), dtype='ushort')
		self.floats = numpy.zeros((), dtype='uint')
		self.pos_bones_p = numpy.zeros((), dtype='ubyte')
		self.ori_bones_p = numpy.zeros((), dtype='ubyte')
		self.scl_bones_p = numpy.zeros((), dtype='ubyte')
		self.pos_bones_delta = numpy.zeros((), dtype='ubyte')
		self.ori_bones_delta = numpy.zeros((), dtype='ubyte')
		self.scl_bones_delta = numpy.zeros((), dtype='ubyte')

		# ?
		self.pad = PadAlign(self.context, self.ref, 4)

		# these are likely a scale reference or factor
		self.floatsa = numpy.zeros((), dtype='float')

		# ?
		self.pad_2 = SmartPadding(self.context, None, None)
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0

		# maybe
		self.scl_bone_count = 0

		# fixed
		self.zeros_18 = numpy.zeros((18), dtype='uint')
		self.count = 0

		# usually 420, or 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, None, None)
		self.zeros = numpy.zeros((self.pos_bone_count), dtype='ubyte')
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = PadAlign(self.context, self.ref_2, 4)

		# these are likely a scale reference or factor
		self.floatsb = numpy.zeros((6), dtype='float')

		# these are likely a scale reference or factor
		self.floats_second = numpy.zeros((self.flag_1, 6), dtype='float')

		# these are likely a scale reference or factor
		self.floats_third = numpy.zeros((6), dtype='float')

		# ?
		self.unk = 0

		# this seems to be vaguely related, but not always there?
		self.extra_pc_zero = 0
		self.repeats = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.ref = Empty(self.context, None, None)
		if self.context.version == 18:
			self.pos_bones = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.pos_bones = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.ori_bones = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.ori_bones = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.scl_bones = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.scl_bones = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.floats = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.floats = numpy.zeros((), dtype='uint')
		self.pos_bones_p = numpy.zeros((), dtype='ubyte')
		self.ori_bones_p = numpy.zeros((), dtype='ubyte')
		self.scl_bones_p = numpy.zeros((), dtype='ubyte')
		if self.arg.pos_bone_min >= 0:
			self.pos_bones_delta = numpy.zeros((), dtype='ubyte')
		if self.arg.ori_bone_min >= 0:
			self.ori_bones_delta = numpy.zeros((), dtype='ubyte')
		if self.arg.scl_bone_min >= 0:
			self.scl_bones_delta = numpy.zeros((), dtype='ubyte')
		self.pad = PadAlign(self.context, self.ref, 4)
		self.floatsa = numpy.zeros((), dtype='float')
		self.pad_2 = SmartPadding(self.context, None, None)
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0
		self.scl_bone_count = 0
		self.zeros_18 = numpy.zeros((18), dtype='uint')
		self.count = 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, None, None)
		self.zeros = numpy.zeros((self.pos_bone_count), dtype='ubyte')
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = PadAlign(self.context, self.ref_2, 4)
		self.floatsb = numpy.zeros((6), dtype='float')
		self.floats_second = numpy.zeros((self.flag_1, 6), dtype='float')
		if self.flag_2 > 1:
			self.floats_third = numpy.zeros((6), dtype='float')
		self.unk = 0
		if self.context.version == 18:
			self.extra_pc_zero = 0
		self.repeats = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.ref = stream.read_type(Empty, (self.context, None, None))
		if self.context.version == 18:
			self.pos_bones = stream.read_ushorts((self.arg.pos_bone_count))
		if not (self.context.version == 18):
			self.pos_bones = stream.read_uints((self.arg.pos_bone_count))
		if self.context.version == 18:
			self.ori_bones = stream.read_ushorts((self.arg.ori_bone_count))
		if not (self.context.version == 18):
			self.ori_bones = stream.read_uints((self.arg.ori_bone_count))
		if self.context.version == 18:
			self.scl_bones = stream.read_ushorts((self.arg.scl_bone_count))
		if not (self.context.version == 18):
			self.scl_bones = stream.read_uints((self.arg.scl_bone_count))
		if self.context.version == 18:
			self.floats = stream.read_ushorts((self.arg.float_count))
		if not (self.context.version == 18):
			self.floats = stream.read_uints((self.arg.float_count))
		self.pos_bones_p = stream.read_ubytes((self.arg.pos_bone_count))
		self.ori_bones_p = stream.read_ubytes((self.arg.ori_bone_count))
		self.scl_bones_p = stream.read_ubytes((self.arg.scl_bone_count))
		if self.arg.pos_bone_min >= 0:
			self.pos_bones_delta = stream.read_ubytes(((self.arg.pos_bone_max - self.arg.pos_bone_min) + 1))
		if self.arg.ori_bone_min >= 0:
			self.ori_bones_delta = stream.read_ubytes(((self.arg.ori_bone_max - self.arg.ori_bone_min) + 1))
		if self.arg.scl_bone_min >= 0:
			self.scl_bones_delta = stream.read_ubytes(((self.arg.scl_bone_max - self.arg.scl_bone_min) + 1))
		self.pad = stream.read_type(PadAlign, (self.context, self.ref, 4))
		self.floatsa = stream.read_floats((self.arg.frame_count, self.arg.float_count))
		self.pad_2 = stream.read_type(SmartPadding, (self.context, None, None))
		self.frame_count = stream.read_uint()
		self.ori_bone_count = stream.read_uint()
		self.pos_bone_count = stream.read_uint()
		self.scl_bone_count = stream.read_uint()
		self.zeros_18 = stream.read_uints((18))
		self.count = stream.read_ushort()
		self.quantisation_level = stream.read_ushort()
		self.ref_2 = stream.read_type(Empty, (self.context, None, None))
		self.zeros = stream.read_ubytes((self.pos_bone_count))
		self.flag_0 = stream.read_ubyte()
		self.flag_1 = stream.read_ubyte()
		self.flag_2 = stream.read_ubyte()
		self.flag_3 = stream.read_ubyte()
		self.anoth_pad = stream.read_type(PadAlign, (self.context, self.ref_2, 4))
		self.floatsb = stream.read_floats((6))
		self.floats_second = stream.read_floats((self.flag_1, 6))
		if self.flag_2 > 1:
			self.floats_third = stream.read_floats((6))
		self.unk = stream.read_uint()
		if self.context.version == 18:
			self.extra_pc_zero = stream.read_uint64()
		self.repeats.read(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.ref)
		if self.context.version == 18:
			stream.write_ushorts(self.pos_bones)
		if not (self.context.version == 18):
			stream.write_uints(self.pos_bones)
		if self.context.version == 18:
			stream.write_ushorts(self.ori_bones)
		if not (self.context.version == 18):
			stream.write_uints(self.ori_bones)
		if self.context.version == 18:
			stream.write_ushorts(self.scl_bones)
		if not (self.context.version == 18):
			stream.write_uints(self.scl_bones)
		if self.context.version == 18:
			stream.write_ushorts(self.floats)
		if not (self.context.version == 18):
			stream.write_uints(self.floats)
		stream.write_ubytes(self.pos_bones_p)
		stream.write_ubytes(self.ori_bones_p)
		stream.write_ubytes(self.scl_bones_p)
		if self.arg.pos_bone_min >= 0:
			stream.write_ubytes(self.pos_bones_delta)
		if self.arg.ori_bone_min >= 0:
			stream.write_ubytes(self.ori_bones_delta)
		if self.arg.scl_bone_min >= 0:
			stream.write_ubytes(self.scl_bones_delta)
		stream.write_type(self.pad)
		stream.write_floats(self.floatsa)
		stream.write_type(self.pad_2)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.ori_bone_count)
		stream.write_uint(self.pos_bone_count)
		stream.write_uint(self.scl_bone_count)
		stream.write_uints(self.zeros_18)
		stream.write_ushort(self.count)
		stream.write_ushort(self.quantisation_level)
		stream.write_type(self.ref_2)
		stream.write_ubytes(self.zeros)
		stream.write_ubyte(self.flag_0)
		stream.write_ubyte(self.flag_1)
		stream.write_ubyte(self.flag_2)
		stream.write_ubyte(self.flag_3)
		stream.write_type(self.anoth_pad)
		stream.write_floats(self.floatsb)
		stream.write_floats(self.floats_second)
		if self.flag_2 > 1:
			stream.write_floats(self.floats_third)
		stream.write_uint(self.unk)
		if self.context.version == 18:
			stream.write_uint64(self.extra_pc_zero)
		self.repeats.write(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiBlock [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ref = {self.ref.__repr__()}'
		s += f'\n	* pos_bones = {self.pos_bones.__repr__()}'
		s += f'\n	* ori_bones = {self.ori_bones.__repr__()}'
		s += f'\n	* scl_bones = {self.scl_bones.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* pos_bones_p = {self.pos_bones_p.__repr__()}'
		s += f'\n	* ori_bones_p = {self.ori_bones_p.__repr__()}'
		s += f'\n	* scl_bones_p = {self.scl_bones_p.__repr__()}'
		s += f'\n	* pos_bones_delta = {self.pos_bones_delta.__repr__()}'
		s += f'\n	* ori_bones_delta = {self.ori_bones_delta.__repr__()}'
		s += f'\n	* scl_bones_delta = {self.scl_bones_delta.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* floatsa = {self.floatsa.__repr__()}'
		s += f'\n	* pad_2 = {self.pad_2.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* ori_bone_count = {self.ori_bone_count.__repr__()}'
		s += f'\n	* pos_bone_count = {self.pos_bone_count.__repr__()}'
		s += f'\n	* scl_bone_count = {self.scl_bone_count.__repr__()}'
		s += f'\n	* zeros_18 = {self.zeros_18.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* quantisation_level = {self.quantisation_level.__repr__()}'
		s += f'\n	* ref_2 = {self.ref_2.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* flag_0 = {self.flag_0.__repr__()}'
		s += f'\n	* flag_1 = {self.flag_1.__repr__()}'
		s += f'\n	* flag_2 = {self.flag_2.__repr__()}'
		s += f'\n	* flag_3 = {self.flag_3.__repr__()}'
		s += f'\n	* anoth_pad = {self.anoth_pad.__repr__()}'
		s += f'\n	* floatsb = {self.floatsb.__repr__()}'
		s += f'\n	* floats_second = {self.floats_second.__repr__()}'
		s += f'\n	* floats_third = {self.floats_third.__repr__()}'
		s += f'\n	* unk = {self.unk.__repr__()}'
		s += f'\n	* extra_pc_zero = {self.extra_pc_zero.__repr__()}'
		s += f'\n	* repeats = {self.repeats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
