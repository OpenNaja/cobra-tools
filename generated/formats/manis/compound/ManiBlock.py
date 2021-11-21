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
		self.indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint16'))
		self.indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint32'))
		self.indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint16'))
		self.indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint32'))
		self.indices_1 = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint16'))
		self.indices_1 = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint32'))
		self.indices_e_2 = numpy.zeros((self.arg.e_2,), dtype=numpy.dtype('uint16'))
		self.indices_e_2 = numpy.zeros((self.arg.e_2,), dtype=numpy.dtype('uint32'))
		self.p_indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint8'))
		self.p_indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint8'))
		self.p_indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint8'))
		self.p_indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint8'))
		self.p_indices_0_b = numpy.zeros(((self.arg.p_indices_c_0_max - self.arg.p_indices_c_0_min) + 1,), dtype=numpy.dtype('uint8'))
		self.p_indices_0_c = numpy.zeros(((self.arg.p_indices_c_1_max - self.arg.p_indices_c_1_min) + 1,), dtype=numpy.dtype('uint8'))

		# ?
		self.pad = PadAlign(self.context, 4, ref)

		# these are likely a scale reference or factor
		self.floatsa = numpy.zeros((self.arg.frame_count, self.arg.e_2,), dtype=numpy.dtype('float32'))

		# ?
		self.pad_2 = SmartPadding(self.context, 0, None)

		# likely
		self.frame_count = 0
		self.c_1 = 0
		self.e = 0

		# fixed
		self.zeros_19 = numpy.zeros((19,), dtype=numpy.dtype('uint32'))
		self.count = 0

		# usually / always 420
		self.four_and_twenty = 0
		self.ref_2 = Empty(self.context, 0, None)
		self.zeros = numpy.zeros((self.c_1,), dtype=numpy.dtype('uint8'))

		# ?
		self.anoth_pad = SmartPadding(self.context, 0, None)

		# these are likely a scale reference or factor
		self.floatsb = numpy.zeros((6,), dtype=numpy.dtype('float32'))

		# ?
		self.unk = 0

		# this seems to be vaguely related, but not always there?
		self.unk_for_e_2 = 0
		self.repeats = Array((self.count,), Repeat, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.ref = Empty(self.context, 0, None)
		if self.context.version == 18:
			self.indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.indices_1 = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.indices_1 = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.indices_e_2 = numpy.zeros((self.arg.e_2,), dtype=numpy.dtype('uint16'))
		if not (self.context.version == 18):
			self.indices_e_2 = numpy.zeros((self.arg.e_2,), dtype=numpy.dtype('uint32'))
		self.p_indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint8'))
		if self.context.version == 18:
			self.p_indices_c_0 = numpy.zeros((self.arg.c_0,), dtype=numpy.dtype('uint8'))
		self.p_indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint8'))
		if self.context.version == 18:
			self.p_indices_c_1 = numpy.zeros((self.arg.c_1,), dtype=numpy.dtype('uint8'))
		self.p_indices_0_b = numpy.zeros(((self.arg.p_indices_c_0_max - self.arg.p_indices_c_0_min) + 1,), dtype=numpy.dtype('uint8'))
		self.p_indices_0_c = numpy.zeros(((self.arg.p_indices_c_1_max - self.arg.p_indices_c_1_min) + 1,), dtype=numpy.dtype('uint8'))
		self.pad = PadAlign(self.context, 4, ref)
		self.floatsa = numpy.zeros((self.arg.frame_count, self.arg.e_2,), dtype=numpy.dtype('float32'))
		self.pad_2 = SmartPadding(self.context, 0, None)
		self.frame_count = 0
		self.c_1 = 0
		self.e = 0
		self.zeros_19 = numpy.zeros((19,), dtype=numpy.dtype('uint32'))
		self.count = 0
		self.four_and_twenty = 0
		self.ref_2 = Empty(self.context, 0, None)
		self.zeros = numpy.zeros((self.c_1,), dtype=numpy.dtype('uint8'))
		self.anoth_pad = SmartPadding(self.context, 0, None)
		self.floatsb = numpy.zeros((6,), dtype=numpy.dtype('float32'))
		self.unk = 0
		if self.arg.e_2:
			self.unk_for_e_2 = 0
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
			instance.indices_c_0 = stream.read_ushorts((instance.arg.c_0,))
		if not (instance.context.version == 18):
			instance.indices_c_0 = stream.read_uints((instance.arg.c_0,))
		if instance.context.version == 18:
			instance.indices_c_1 = stream.read_ushorts((instance.arg.c_1,))
		if not (instance.context.version == 18):
			instance.indices_c_1 = stream.read_uints((instance.arg.c_1,))
		if instance.context.version == 18:
			instance.indices_1 = stream.read_ushorts((instance.arg.name_count,))
		if not (instance.context.version == 18):
			instance.indices_1 = stream.read_uints((instance.arg.name_count,))
		if instance.context.version == 18:
			instance.indices_e_2 = stream.read_ushorts((instance.arg.e_2,))
		if not (instance.context.version == 18):
			instance.indices_e_2 = stream.read_uints((instance.arg.e_2,))
		instance.p_indices_c_0 = stream.read_ubytes((instance.arg.c_0,))
		if instance.context.version == 18:
			instance.p_indices_c_0 = stream.read_ubytes((instance.arg.c_0,))
		instance.p_indices_c_1 = stream.read_ubytes((instance.arg.c_1,))
		if instance.context.version == 18:
			instance.p_indices_c_1 = stream.read_ubytes((instance.arg.c_1,))
		instance.p_indices_0_b = stream.read_ubytes(((instance.arg.p_indices_c_0_max - instance.arg.p_indices_c_0_min) + 1,))
		instance.p_indices_0_c = stream.read_ubytes(((instance.arg.p_indices_c_1_max - instance.arg.p_indices_c_1_min) + 1,))
		instance.pad = PadAlign.from_stream(stream, instance.context, 4, ref)
		instance.floatsa = stream.read_floats((instance.arg.frame_count, instance.arg.e_2,))
		instance.pad_2 = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.frame_count = stream.read_uint()
		instance.c_1 = stream.read_uint()
		instance.e = stream.read_uint()
		instance.zeros_19 = stream.read_uints((19,))
		instance.count = stream.read_ushort()
		instance.four_and_twenty = stream.read_ushort()
		instance.ref_2 = Empty.from_stream(stream, instance.context, 0, None)
		instance.zeros = stream.read_ubytes((instance.c_1,))
		instance.anoth_pad = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.floatsb = stream.read_floats((6,))
		instance.unk = stream.read_uint()
		if instance.arg.e_2:
			instance.unk_for_e_2 = stream.read_uint64()
		instance.repeats = Array.from_stream(stream, (instance.count,), Repeat, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		Empty.to_stream(stream, instance.ref)
		if instance.context.version == 18:
			stream.write_ushorts(instance.indices_c_0)
		if not (instance.context.version == 18):
			stream.write_uints(instance.indices_c_0)
		if instance.context.version == 18:
			stream.write_ushorts(instance.indices_c_1)
		if not (instance.context.version == 18):
			stream.write_uints(instance.indices_c_1)
		if instance.context.version == 18:
			stream.write_ushorts(instance.indices_1)
		if not (instance.context.version == 18):
			stream.write_uints(instance.indices_1)
		if instance.context.version == 18:
			stream.write_ushorts(instance.indices_e_2)
		if not (instance.context.version == 18):
			stream.write_uints(instance.indices_e_2)
		stream.write_ubytes(instance.p_indices_c_0)
		if instance.context.version == 18:
			stream.write_ubytes(instance.p_indices_c_0)
		stream.write_ubytes(instance.p_indices_c_1)
		if instance.context.version == 18:
			stream.write_ubytes(instance.p_indices_c_1)
		stream.write_ubytes(instance.p_indices_0_b)
		stream.write_ubytes(instance.p_indices_0_c)
		PadAlign.to_stream(stream, instance.pad)
		stream.write_floats(instance.floatsa)
		SmartPadding.to_stream(stream, instance.pad_2)
		stream.write_uint(instance.frame_count)
		stream.write_uint(instance.c_1)
		stream.write_uint(instance.e)
		stream.write_uints(instance.zeros_19)
		stream.write_ushort(instance.count)
		stream.write_ushort(instance.four_and_twenty)
		Empty.to_stream(stream, instance.ref_2)
		stream.write_ubytes(instance.zeros)
		SmartPadding.to_stream(stream, instance.anoth_pad)
		stream.write_floats(instance.floatsb)
		stream.write_uint(instance.unk)
		if instance.arg.e_2:
			stream.write_uint64(instance.unk_for_e_2)
		Array.to_stream(stream, instance.repeats, (instance.count,),Repeat, instance.context, 0, None)

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
		s += f'\n	* indices_c_0 = {self.indices_c_0.__repr__()}'
		s += f'\n	* indices_c_1 = {self.indices_c_1.__repr__()}'
		s += f'\n	* indices_1 = {self.indices_1.__repr__()}'
		s += f'\n	* indices_e_2 = {self.indices_e_2.__repr__()}'
		s += f'\n	* p_indices_c_0 = {self.p_indices_c_0.__repr__()}'
		s += f'\n	* p_indices_c_1 = {self.p_indices_c_1.__repr__()}'
		s += f'\n	* p_indices_0_b = {self.p_indices_0_b.__repr__()}'
		s += f'\n	* p_indices_0_c = {self.p_indices_0_c.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* floatsa = {self.floatsa.__repr__()}'
		s += f'\n	* pad_2 = {self.pad_2.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* c_1 = {self.c_1.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* zeros_19 = {self.zeros_19.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* four_and_twenty = {self.four_and_twenty.__repr__()}'
		s += f'\n	* ref_2 = {self.ref_2.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* anoth_pad = {self.anoth_pad.__repr__()}'
		s += f'\n	* floatsb = {self.floatsb.__repr__()}'
		s += f'\n	* unk = {self.unk.__repr__()}'
		s += f'\n	* unk_for_e_2 = {self.unk_for_e_2.__repr__()}'
		s += f'\n	* repeats = {self.repeats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
