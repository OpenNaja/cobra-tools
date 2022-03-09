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
		self.indices_pos_bone = numpy.zeros((), dtype='ushort')
		self.indices_pos_bone = numpy.zeros((), dtype='uint')
		self.indices_ori_bone = numpy.zeros((), dtype='ushort')
		self.indices_ori_bone = numpy.zeros((), dtype='uint')
		self.indices_1 = numpy.zeros((), dtype='ushort')
		self.indices_1 = numpy.zeros((), dtype='uint')
		self.indices_float = numpy.zeros((), dtype='ushort')
		self.indices_float = numpy.zeros((), dtype='uint')
		self.p_indices_pos_bone = numpy.zeros((), dtype='ubyte')
		self.p_indices_pos_bone = numpy.zeros((), dtype='ubyte')
		self.p_indices_ori_bone = numpy.zeros((), dtype='ubyte')
		self.p_indices_ori_bone = numpy.zeros((), dtype='ubyte')
		self.p_indices_0_b = numpy.zeros((), dtype='ubyte')
		self.p_indices_0_c = numpy.zeros((), dtype='ubyte')

		# ?
		self.pad = PadAlign(self.context, self.ref, 4)

		# these are likely a scale reference or factor
		self.floatsa = numpy.zeros((), dtype='float')

		# ?
		self.pad_2 = SmartPadding(self.context, None, None)

		# likely
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0

		# fixed
		self.zeros_19 = numpy.zeros((19), dtype='uint')
		self.count = 0

		# usually 420, or 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, None, None)
		self.zeros = numpy.zeros((self.pos_bone_count), dtype='ubyte')
		self.flags = numpy.zeros((4), dtype='ubyte')
		self.anoth_pad = PadAlign(self.context, self.ref_2, 4)

		# these are likely a scale reference or factor
		self.floatsb = numpy.zeros((6), dtype='float')

		# ?
		self.unk = 0

		# this seems to be vaguely related, but not always there?
		self.unk_for_float_count = 0
		self.repeats = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.ref = Empty(self.context, None, None)
		if self.context.version == 18:
			self.indices_pos_bone = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_pos_bone = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.indices_ori_bone = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_ori_bone = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.indices_1 = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_1 = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.indices_float = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_float = numpy.zeros((), dtype='uint')
		self.p_indices_pos_bone = numpy.zeros((), dtype='ubyte')
		if self.context.version == 18:
			self.p_indices_pos_bone = numpy.zeros((), dtype='ubyte')
		self.p_indices_ori_bone = numpy.zeros((), dtype='ubyte')
		if self.context.version == 18:
			self.p_indices_ori_bone = numpy.zeros((), dtype='ubyte')
		self.p_indices_0_b = numpy.zeros((), dtype='ubyte')
		self.p_indices_0_c = numpy.zeros((), dtype='ubyte')
		self.pad = PadAlign(self.context, self.ref, 4)
		self.floatsa = numpy.zeros((), dtype='float')
		self.pad_2 = SmartPadding(self.context, None, None)
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0
		self.zeros_19 = numpy.zeros((19), dtype='uint')
		self.count = 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, None, None)
		self.zeros = numpy.zeros((self.pos_bone_count), dtype='ubyte')
		self.flags = numpy.zeros((4), dtype='ubyte')
		self.anoth_pad = PadAlign(self.context, self.ref_2, 4)
		self.floatsb = numpy.zeros((6), dtype='float')
		self.unk = 0
		if self.arg.float_count:
			self.unk_for_float_count = 0
		self.repeats = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.ref = stream.read_type(Empty, (self.context, None, None))
		if self.context.version == 18:
			self.indices_pos_bone = stream.read_ushorts((self.arg.pos_bone_count))
		if not (self.context.version == 18):
			self.indices_pos_bone = stream.read_uints((self.arg.pos_bone_count))
		if self.context.version == 18:
			self.indices_ori_bone = stream.read_ushorts((self.arg.ori_bone_count))
		if not (self.context.version == 18):
			self.indices_ori_bone = stream.read_uints((self.arg.ori_bone_count))
		if self.context.version == 18:
			self.indices_1 = stream.read_ushorts((self.arg.name_count))
		if not (self.context.version == 18):
			self.indices_1 = stream.read_uints((self.arg.name_count))
		if self.context.version == 18:
			self.indices_float = stream.read_ushorts((self.arg.float_count))
		if not (self.context.version == 18):
			self.indices_float = stream.read_uints((self.arg.float_count))
		self.p_indices_pos_bone = stream.read_ubytes((self.arg.pos_bone_count))
		if self.context.version == 18:
			self.p_indices_pos_bone = stream.read_ubytes((self.arg.pos_bone_count))
		self.p_indices_ori_bone = stream.read_ubytes((self.arg.ori_bone_count))
		if self.context.version == 18:
			self.p_indices_ori_bone = stream.read_ubytes((self.arg.ori_bone_count))
		self.p_indices_0_b = stream.read_ubytes(((self.arg.pos_bone_max - self.arg.pos_bone_min) + 1))
		self.p_indices_0_c = stream.read_ubytes(((self.arg.ori_bone_max - self.arg.ori_bone_min) + 1))
		self.pad = stream.read_type(PadAlign, (self.context, self.ref, 4))
		self.floatsa = stream.read_floats((self.arg.frame_count, self.arg.float_count))
		self.pad_2 = stream.read_type(SmartPadding, (self.context, None, None))
		self.frame_count = stream.read_uint()
		self.ori_bone_count = stream.read_uint()
		self.pos_bone_count = stream.read_uint()
		self.zeros_19 = stream.read_uints((19))
		self.count = stream.read_ushort()
		self.quantisation_level = stream.read_ushort()
		self.ref_2 = stream.read_type(Empty, (self.context, None, None))
		self.zeros = stream.read_ubytes((self.pos_bone_count))
		self.flags = stream.read_ubytes((4))
		self.anoth_pad = stream.read_type(PadAlign, (self.context, self.ref_2, 4))
		self.floatsb = stream.read_floats((6))
		self.unk = stream.read_uint()
		if self.arg.float_count:
			self.unk_for_float_count = stream.read_uint64()
		self.repeats.read(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.ref)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_pos_bone)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_pos_bone)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_ori_bone)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_ori_bone)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_1)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_1)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_float)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_float)
		stream.write_ubytes(self.p_indices_pos_bone)
		if self.context.version == 18:
			stream.write_ubytes(self.p_indices_pos_bone)
		stream.write_ubytes(self.p_indices_ori_bone)
		if self.context.version == 18:
			stream.write_ubytes(self.p_indices_ori_bone)
		stream.write_ubytes(self.p_indices_0_b)
		stream.write_ubytes(self.p_indices_0_c)
		stream.write_type(self.pad)
		stream.write_floats(self.floatsa)
		stream.write_type(self.pad_2)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.ori_bone_count)
		stream.write_uint(self.pos_bone_count)
		stream.write_uints(self.zeros_19)
		stream.write_ushort(self.count)
		stream.write_ushort(self.quantisation_level)
		stream.write_type(self.ref_2)
		stream.write_ubytes(self.zeros)
		stream.write_ubytes(self.flags)
		stream.write_type(self.anoth_pad)
		stream.write_floats(self.floatsb)
		stream.write_uint(self.unk)
		if self.arg.float_count:
			stream.write_uint64(self.unk_for_float_count)
		self.repeats.write(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiBlock [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ref = {self.ref.__repr__()}'
		s += f'\n	* indices_pos_bone = {self.indices_pos_bone.__repr__()}'
		s += f'\n	* indices_ori_bone = {self.indices_ori_bone.__repr__()}'
		s += f'\n	* indices_1 = {self.indices_1.__repr__()}'
		s += f'\n	* indices_float = {self.indices_float.__repr__()}'
		s += f'\n	* p_indices_pos_bone = {self.p_indices_pos_bone.__repr__()}'
		s += f'\n	* p_indices_ori_bone = {self.p_indices_ori_bone.__repr__()}'
		s += f'\n	* p_indices_0_b = {self.p_indices_0_b.__repr__()}'
		s += f'\n	* p_indices_0_c = {self.p_indices_0_c.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* floatsa = {self.floatsa.__repr__()}'
		s += f'\n	* pad_2 = {self.pad_2.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* ori_bone_count = {self.ori_bone_count.__repr__()}'
		s += f'\n	* pos_bone_count = {self.pos_bone_count.__repr__()}'
		s += f'\n	* zeros_19 = {self.zeros_19.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* quantisation_level = {self.quantisation_level.__repr__()}'
		s += f'\n	* ref_2 = {self.ref_2.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* flags = {self.flags.__repr__()}'
		s += f'\n	* anoth_pad = {self.anoth_pad.__repr__()}'
		s += f'\n	* floatsb = {self.floatsb.__repr__()}'
		s += f'\n	* unk = {self.unk.__repr__()}'
		s += f'\n	* unk_for_float_count = {self.unk_for_float_count.__repr__()}'
		s += f'\n	* repeats = {self.repeats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
