import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.manis.compound.Empty import Empty
from generated.formats.manis.compound.PadAlign import PadAlign
from generated.formats.manis.compound.Repeat import Repeat
from generated.formats.manis.compound.SmartPadding import SmartPadding


class ManiBlock:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ref = Empty(self.context, 0, None)
		self.pos_bones = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint16'))
		self.pos_bones = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint32'))
		self.ori_bones = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint16'))
		self.ori_bones = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint32'))
		self.scl_bones = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint16'))
		self.scl_bones = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint32'))
		self.floats = numpy.zeros((self.arg.float_count,), dtype=numpy.dtype('uint16'))
		self.floats = numpy.zeros((self.arg.float_count,), dtype=numpy.dtype('uint32'))
		self.pos_bones_p = numpy.zeros((self.arg.pos_bone_count,), dtype=numpy.dtype('uint8'))
		self.ori_bones_p = numpy.zeros((self.arg.ori_bone_count,), dtype=numpy.dtype('uint8'))
		self.scl_bones_p = numpy.zeros((self.arg.scl_bone_count,), dtype=numpy.dtype('uint8'))
		self.pos_bones_delta = numpy.zeros(((self.arg.pos_bone_max - self.arg.pos_bone_min) + 1,), dtype=numpy.dtype('uint8'))
		self.ori_bones_delta = numpy.zeros(((self.arg.ori_bone_max - self.arg.ori_bone_min) + 1,), dtype=numpy.dtype('uint8'))
		self.scl_bones_delta = numpy.zeros(((self.arg.scl_bone_max - self.arg.scl_bone_min) + 1,), dtype=numpy.dtype('uint8'))

		# ?
		self.pad = PadAlign(self.context, self.ref, 4)

		# these are likely a scale reference or factor
		self.floatsa = numpy.zeros((self.arg.frame_count, self.arg.float_count,), dtype=numpy.dtype('float32'))

		# ?
		self.pad_2 = SmartPadding(self.context, 0, None)
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0

		# maybe
		self.scl_bone_count = 0

		# fixed
		self.zeros_18 = numpy.zeros((18,), dtype=numpy.dtype('uint32'))
		self.count = 0

		# usually 420, or 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, 0, None)
		self.zeros = numpy.zeros((self.pos_bone_count,), dtype=numpy.dtype('uint8'))
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = PadAlign(self.context, self.ref_2, 4)

		# these are likely a scale reference or factor
		self.floatsb = numpy.zeros((6,), dtype=numpy.dtype('float32'))

		# these are likely a scale reference or factor
		self.floats_second = numpy.zeros((self.flag_1, 6,), dtype=numpy.dtype('float32'))

		# these are likely a scale reference or factor
		self.floats_third = numpy.zeros((6,), dtype=numpy.dtype('float32'))

		# ?
		self.unk = 0

		# this seems to be vaguely related, but not always there?
		self.extra_pc_zero = 0
		self.repeats = Array((self.count,), Repeat, self.context, 0, None)
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
		self.pad = PadAlign(self.context, self.ref, 4)
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
		self.anoth_pad = PadAlign(self.context, self.ref_2, 4)
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
		instance.pad = PadAlign.from_stream(stream, instance.context, instance.ref, 4)
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
		instance.anoth_pad = PadAlign.from_stream(stream, instance.context, instance.ref_2, 4)
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
