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
		self.ref = Empty(context, None, None)
		if self.context.version == 18:
			self.indices_c_2 = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_c_2 = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.indices_0 = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_0 = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.indices_1 = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_1 = numpy.zeros((), dtype='uint')
		if self.context.version == 18:
			self.indices_e_2 = numpy.zeros((), dtype='ushort')
		if not (self.context.version == 18):
			self.indices_e_2 = numpy.zeros((), dtype='uint')
		self.p_indices_00 = numpy.zeros((), dtype='ubyte')
		if self.context.version == 18:
			self.p_indices_00 = numpy.zeros((), dtype='ubyte')
		self.p_indices_0 = numpy.zeros((), dtype='ubyte')
		if self.context.version == 18:
			self.p_indices_0 = numpy.zeros((), dtype='ubyte')
		self.p_indices_0_b = numpy.zeros((), dtype='ubyte')
		if self.arg.e_2 > 0:
			self.p_indices_0_c = numpy.zeros((), dtype='ubyte')

		# ?
		self.pad = PadAlign(context, self.ref, 4)

		# these are likely a scale reference or factor
		self.floatsa = numpy.zeros((), dtype='float')

		# ?
		self.pad_2 = SmartPadding(context, None, None)

		# likely
		self.frame_count = 0
		self.c = 0
		self.e = 0

		# fixed
		self.zeros_19 = numpy.zeros((19), dtype='uint')
		self.count = 0

		# usually / always 420
		self.four_and_twenty = 0
		self.ref_2 = Empty(context, None, None)
		self.zeros = numpy.zeros((self.c), dtype='ubyte')

		# ?
		self.anoth_pad = SmartPadding(context, None, None)

		# these are likely a scale reference or factor
		self.floatsb = numpy.zeros((6), dtype='float')
		self.repeats = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.ref = stream.read_type(Empty, (self.context, None, None))
		if self.context.version == 18:
			self.indices_c_2 = stream.read_ushorts((self.arg.c_2))
		if not (self.context.version == 18):
			self.indices_c_2 = stream.read_uints((self.arg.c_2))
		if self.context.version == 18:
			self.indices_0 = stream.read_ushorts((self.arg.c))
		if not (self.context.version == 18):
			self.indices_0 = stream.read_uints((self.arg.c))
		if self.context.version == 18:
			self.indices_1 = stream.read_ushorts((self.arg.name_count))
		if not (self.context.version == 18):
			self.indices_1 = stream.read_uints((self.arg.name_count))
		if self.context.version == 18:
			self.indices_e_2 = stream.read_ushorts((self.arg.e_2))
		if not (self.context.version == 18):
			self.indices_e_2 = stream.read_uints((self.arg.e_2))
		self.p_indices_00 = stream.read_ubytes((self.arg.c_2))
		if self.context.version == 18:
			self.p_indices_00 = stream.read_ubytes((self.arg.c_2))
		self.p_indices_0 = stream.read_ubytes((self.arg.c))
		if self.context.version == 18:
			self.p_indices_0 = stream.read_ubytes((self.arg.c))
		self.p_indices_0_b = stream.read_ubytes((self.arg.e))
		if self.arg.e_2 > 0:
			self.p_indices_0_c = stream.read_ubytes((self.arg.e))
		self.pad = stream.read_type(PadAlign, (self.context, self.ref, 4))
		self.floatsa = stream.read_floats((self.arg.frame_count, self.arg.e_2))
		self.pad_2 = stream.read_type(SmartPadding, (self.context, None, None))
		self.frame_count = stream.read_uint()
		self.c = stream.read_uint()
		self.e = stream.read_uint()
		self.zeros_19 = stream.read_uints((19))
		self.count = stream.read_ushort()
		self.four_and_twenty = stream.read_ushort()
		self.ref_2 = stream.read_type(Empty, (self.context, None, None))
		self.zeros = stream.read_ubytes((self.c))
		self.anoth_pad = stream.read_type(SmartPadding, (self.context, None, None))
		self.floatsb = stream.read_floats((6))
		self.repeats.read(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.ref)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_c_2)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_c_2)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_0)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_0)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_1)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_1)
		if self.context.version == 18:
			stream.write_ushorts(self.indices_e_2)
		if not (self.context.version == 18):
			stream.write_uints(self.indices_e_2)
		stream.write_ubytes(self.p_indices_00)
		if self.context.version == 18:
			stream.write_ubytes(self.p_indices_00)
		stream.write_ubytes(self.p_indices_0)
		if self.context.version == 18:
			stream.write_ubytes(self.p_indices_0)
		stream.write_ubytes(self.p_indices_0_b)
		if self.arg.e_2 > 0:
			stream.write_ubytes(self.p_indices_0_c)
		stream.write_type(self.pad)
		stream.write_floats(self.floatsa)
		stream.write_type(self.pad_2)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.c)
		stream.write_uint(self.e)
		stream.write_uints(self.zeros_19)
		stream.write_ushort(self.count)
		stream.write_ushort(self.four_and_twenty)
		stream.write_type(self.ref_2)
		stream.write_ubytes(self.zeros)
		stream.write_type(self.anoth_pad)
		stream.write_floats(self.floatsb)
		self.repeats.write(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiBlock [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ref = {self.ref.__repr__()}'
		s += f'\n	* indices_c_2 = {self.indices_c_2.__repr__()}'
		s += f'\n	* indices_0 = {self.indices_0.__repr__()}'
		s += f'\n	* indices_1 = {self.indices_1.__repr__()}'
		s += f'\n	* indices_e_2 = {self.indices_e_2.__repr__()}'
		s += f'\n	* p_indices_00 = {self.p_indices_00.__repr__()}'
		s += f'\n	* p_indices_0 = {self.p_indices_0.__repr__()}'
		s += f'\n	* p_indices_0_b = {self.p_indices_0_b.__repr__()}'
		s += f'\n	* p_indices_0_c = {self.p_indices_0_c.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* floatsa = {self.floatsa.__repr__()}'
		s += f'\n	* pad_2 = {self.pad_2.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* c = {self.c.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* zeros_19 = {self.zeros_19.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* four_and_twenty = {self.four_and_twenty.__repr__()}'
		s += f'\n	* ref_2 = {self.ref_2.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* anoth_pad = {self.anoth_pad.__repr__()}'
		s += f'\n	* floatsb = {self.floatsb.__repr__()}'
		s += f'\n	* repeats = {self.repeats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
