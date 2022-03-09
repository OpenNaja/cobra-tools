import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class ManiInfo:

	"""
	288 bytes for JWE / PZ
	312 bytes for PC
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.duration = 0
		self.frame_count = 0
		self.b = 0

		# rest
		self.zeros_0 = numpy.zeros((6), dtype='ushort')
		self.pos_bone_count = 0
		self.ori_bone_count = 0
		self.name_count = 0

		# rest
		self.zeros_1 = numpy.zeros((3), dtype='ushort')
		self.float_count = 0

		# always FF FF
		self.minus_1_a = 0
		self.e = 0
		self.extra_pc = numpy.zeros((5), dtype='ushort')
		self.g = 0

		# rest 228 bytes
		self.zeros_2 = numpy.zeros((57), dtype='uint')

		# rest 14 bytes
		self.extra_zeros_pc = numpy.zeros((7), dtype='ushort')
		self.pos_bone_min = 0
		self.pos_bone_max = 0
		self.ori_bone_min = 0
		self.ori_bone_max = 0

		# always FF
		self.minus_1_b = 0

		# always 00
		self.zero = 0
		self.c_2 = 0
		self.c_3 = 0
		self.c_4 = 0
		self.c_5 = 0
		self.zeros_end = numpy.zeros((3), dtype='ushort')
		self.set_defaults()

	def set_defaults(self):
		self.duration = 0
		self.frame_count = 0
		self.b = 0
		self.zeros_0 = numpy.zeros((6), dtype='ushort')
		self.pos_bone_count = 0
		self.ori_bone_count = 0
		self.name_count = 0
		self.zeros_1 = numpy.zeros((3), dtype='ushort')
		self.float_count = 0
		self.minus_1_a = 0
		self.e = 0
		if self.context.version == 18:
			self.extra_pc = numpy.zeros((5), dtype='ushort')
		self.g = 0
		self.zeros_2 = numpy.zeros((57), dtype='uint')
		if self.context.version == 18:
			self.extra_zeros_pc = numpy.zeros((7), dtype='ushort')
		self.pos_bone_min = 0
		self.pos_bone_max = 0
		self.ori_bone_min = 0
		self.ori_bone_max = 0
		self.minus_1_b = 0
		self.zero = 0
		if not (self.context.version == 18):
			self.c_2 = 0
		if not (self.context.version == 18):
			self.c_3 = 0
		if not (self.context.version == 18):
			self.c_4 = 0
		if not (self.context.version == 18):
			self.c_5 = 0
		if not (self.context.version == 18):
			self.zeros_end = numpy.zeros((3), dtype='ushort')

	def read(self, stream):
		self.io_start = stream.tell()
		self.duration = stream.read_float()
		self.frame_count = stream.read_uint()
		self.b = stream.read_uint()
		self.zeros_0 = stream.read_ushorts((6))
		self.pos_bone_count = stream.read_ushort()
		self.ori_bone_count = stream.read_ushort()
		self.name_count = stream.read_ushort()
		self.zeros_1 = stream.read_ushorts((3))
		self.float_count = stream.read_ushort()
		self.minus_1_a = stream.read_short()
		self.e = stream.read_ushort()
		if self.context.version == 18:
			self.extra_pc = stream.read_ushorts((5))
		self.g = stream.read_ushort()
		self.zeros_2 = stream.read_uints((57))
		if self.context.version == 18:
			self.extra_zeros_pc = stream.read_ushorts((7))
		self.pos_bone_min = stream.read_ubyte()
		self.pos_bone_max = stream.read_ubyte()
		self.ori_bone_min = stream.read_ubyte()
		self.ori_bone_max = stream.read_ubyte()
		self.minus_1_b = stream.read_byte()
		self.zero = stream.read_byte()
		if not (self.context.version == 18):
			self.c_2 = stream.read_ubyte()
			self.c_3 = stream.read_ubyte()
		if not (self.context.version == 18):
			self.c_4 = stream.read_ubyte()
			self.c_5 = stream.read_ubyte()
		if not (self.context.version == 18):
			self.zeros_end = stream.read_ushorts((3))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_float(self.duration)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.b)
		stream.write_ushorts(self.zeros_0)
		stream.write_ushort(self.pos_bone_count)
		stream.write_ushort(self.ori_bone_count)
		stream.write_ushort(self.name_count)
		stream.write_ushorts(self.zeros_1)
		stream.write_ushort(self.float_count)
		stream.write_short(self.minus_1_a)
		stream.write_ushort(self.e)
		if self.context.version == 18:
			stream.write_ushorts(self.extra_pc)
		stream.write_ushort(self.g)
		stream.write_uints(self.zeros_2)
		if self.context.version == 18:
			stream.write_ushorts(self.extra_zeros_pc)
		stream.write_ubyte(self.pos_bone_min)
		stream.write_ubyte(self.pos_bone_max)
		stream.write_ubyte(self.ori_bone_min)
		stream.write_ubyte(self.ori_bone_max)
		stream.write_byte(self.minus_1_b)
		stream.write_byte(self.zero)
		if not (self.context.version == 18):
			stream.write_ubyte(self.c_2)
			stream.write_ubyte(self.c_3)
		if not (self.context.version == 18):
			stream.write_ubyte(self.c_4)
			stream.write_ubyte(self.c_5)
		if not (self.context.version == 18):
			stream.write_ushorts(self.zeros_end)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* duration = {self.duration.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* pos_bone_count = {self.pos_bone_count.__repr__()}'
		s += f'\n	* ori_bone_count = {self.ori_bone_count.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* float_count = {self.float_count.__repr__()}'
		s += f'\n	* minus_1_a = {self.minus_1_a.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* extra_pc = {self.extra_pc.__repr__()}'
		s += f'\n	* g = {self.g.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* extra_zeros_pc = {self.extra_zeros_pc.__repr__()}'
		s += f'\n	* pos_bone_min = {self.pos_bone_min.__repr__()}'
		s += f'\n	* pos_bone_max = {self.pos_bone_max.__repr__()}'
		s += f'\n	* ori_bone_min = {self.ori_bone_min.__repr__()}'
		s += f'\n	* ori_bone_max = {self.ori_bone_max.__repr__()}'
		s += f'\n	* minus_1_b = {self.minus_1_b.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* c_2 = {self.c_2.__repr__()}'
		s += f'\n	* c_3 = {self.c_3.__repr__()}'
		s += f'\n	* c_4 = {self.c_4.__repr__()}'
		s += f'\n	* c_5 = {self.c_5.__repr__()}'
		s += f'\n	* zeros_end = {self.zeros_end.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
