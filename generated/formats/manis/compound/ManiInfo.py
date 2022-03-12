import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class ManiInfo:

	"""
	288 bytes for JWE / PZ
	304 bytes for PC
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

		# ?
		self.b = 0
		self.zeros_0 = numpy.zeros((6), dtype='ushort')
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
		self.zeros_2 = numpy.zeros((57), dtype='uint')

		# rest 14 bytes
		self.extra_zeros_pc = numpy.zeros((6), dtype='ushort')
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
		self.set_defaults()

	def set_defaults(self):
		self.duration = 0
		self.frame_count = 0
		self.b = 0
		self.zeros_0 = numpy.zeros((6), dtype='ushort')
		if self.context.version == 18:
			self.extra_pc_1 = 0
		self.pos_bone_count = 0
		self.ori_bone_count = 0
		self.scl_bone_count = 0
		if self.context.version == 18:
			self.extra_pc = 0
		if self.context.version == 18:
			self.pos_bone_count_repeat = 0
		if self.context.version == 18:
			self.ori_bone_count_repeat = 0
		if self.context.version == 18:
			self.scl_bone_count_repeat = 0
		self.zeros_1 = 0
		if not (self.context.version == 18):
			self.zeros_1_new = 0
		self.float_count = 0
		self.count_a = 0
		self.count_b = 0
		self.target_bone_count = 0
		self.g = 0
		self.zeros_2 = numpy.zeros((57), dtype='uint')
		if self.context.version == 18:
			self.extra_zeros_pc = numpy.zeros((6), dtype='ushort')
		self.pos_bone_min = 0
		self.pos_bone_max = 0
		self.ori_bone_min = 0
		self.ori_bone_max = 0
		self.scl_bone_min = 0
		self.scl_bone_max = 0
		if not (self.context.version == 18):
			self.pos_bone_count_related = 0
		if not (self.context.version == 18):
			self.pos_bone_count_repeat = 0
		if not (self.context.version == 18):
			self.ori_bone_count_related = 0
		if not (self.context.version == 18):
			self.ori_bone_count_repeat = 0
		if not (self.context.version == 18):
			self.scl_bone_count_related = 0
		if not (self.context.version == 18):
			self.scl_bone_count_repeat = 0
		if not (self.context.version == 18):
			self.zeros_end = 0
		self.zero_2_end = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.duration = stream.read_float()
		self.frame_count = stream.read_uint()
		self.b = stream.read_uint()
		self.zeros_0 = stream.read_ushorts((6))
		if self.context.version == 18:
			self.extra_pc_1 = stream.read_ushort()
		self.pos_bone_count = stream.read_ushort()
		self.ori_bone_count = stream.read_ushort()
		self.scl_bone_count = stream.read_ushort()
		if self.context.version == 18:
			self.extra_pc = stream.read_uint64()
			self.pos_bone_count_repeat = stream.read_ushort()
		if self.context.version == 18:
			self.ori_bone_count_repeat = stream.read_ushort()
			self.scl_bone_count_repeat = stream.read_ushort()
		self.zeros_1 = stream.read_ushort()
		if not (self.context.version == 18):
			self.zeros_1_new = stream.read_uint()
		self.float_count = stream.read_ushort()
		self.count_a = stream.read_ubyte()
		self.count_b = stream.read_ubyte()
		self.target_bone_count = stream.read_ushort()
		self.g = stream.read_ushort()
		self.zeros_2 = stream.read_uints((57))
		if self.context.version == 18:
			self.extra_zeros_pc = stream.read_ushorts((6))
		self.pos_bone_min = stream.read_ubyte()
		self.pos_bone_max = stream.read_ubyte()
		self.ori_bone_min = stream.read_ubyte()
		self.ori_bone_max = stream.read_ubyte()
		self.scl_bone_min = stream.read_ubyte()
		self.scl_bone_max = stream.read_ubyte()
		if not (self.context.version == 18):
			self.pos_bone_count_related = stream.read_ubyte()
			self.pos_bone_count_repeat = stream.read_ubyte()
		if not (self.context.version == 18):
			self.ori_bone_count_related = stream.read_ubyte()
			self.ori_bone_count_repeat = stream.read_ubyte()
		if not (self.context.version == 18):
			self.scl_bone_count_related = stream.read_ubyte()
			self.scl_bone_count_repeat = stream.read_ubyte()
		if not (self.context.version == 18):
			self.zeros_end = stream.read_ushort()
		self.zero_2_end = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_float(self.duration)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.b)
		stream.write_ushorts(self.zeros_0)
		if self.context.version == 18:
			stream.write_ushort(self.extra_pc_1)
		stream.write_ushort(self.pos_bone_count)
		stream.write_ushort(self.ori_bone_count)
		stream.write_ushort(self.scl_bone_count)
		if self.context.version == 18:
			stream.write_uint64(self.extra_pc)
			stream.write_ushort(self.pos_bone_count_repeat)
		if self.context.version == 18:
			stream.write_ushort(self.ori_bone_count_repeat)
			stream.write_ushort(self.scl_bone_count_repeat)
		stream.write_ushort(self.zeros_1)
		if not (self.context.version == 18):
			stream.write_uint(self.zeros_1_new)
		stream.write_ushort(self.float_count)
		stream.write_ubyte(self.count_a)
		stream.write_ubyte(self.count_b)
		stream.write_ushort(self.target_bone_count)
		stream.write_ushort(self.g)
		stream.write_uints(self.zeros_2)
		if self.context.version == 18:
			stream.write_ushorts(self.extra_zeros_pc)
		stream.write_ubyte(self.pos_bone_min)
		stream.write_ubyte(self.pos_bone_max)
		stream.write_ubyte(self.ori_bone_min)
		stream.write_ubyte(self.ori_bone_max)
		stream.write_ubyte(self.scl_bone_min)
		stream.write_ubyte(self.scl_bone_max)
		if not (self.context.version == 18):
			stream.write_ubyte(self.pos_bone_count_related)
			stream.write_ubyte(self.pos_bone_count_repeat)
		if not (self.context.version == 18):
			stream.write_ubyte(self.ori_bone_count_related)
			stream.write_ubyte(self.ori_bone_count_repeat)
		if not (self.context.version == 18):
			stream.write_ubyte(self.scl_bone_count_related)
			stream.write_ubyte(self.scl_bone_count_repeat)
		if not (self.context.version == 18):
			stream.write_ushort(self.zeros_end)
		stream.write_ushort(self.zero_2_end)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* duration = {self.duration.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* extra_pc_1 = {self.extra_pc_1.__repr__()}'
		s += f'\n	* pos_bone_count = {self.pos_bone_count.__repr__()}'
		s += f'\n	* ori_bone_count = {self.ori_bone_count.__repr__()}'
		s += f'\n	* scl_bone_count = {self.scl_bone_count.__repr__()}'
		s += f'\n	* extra_pc = {self.extra_pc.__repr__()}'
		s += f'\n	* pos_bone_count_repeat = {self.pos_bone_count_repeat.__repr__()}'
		s += f'\n	* ori_bone_count_repeat = {self.ori_bone_count_repeat.__repr__()}'
		s += f'\n	* scl_bone_count_repeat = {self.scl_bone_count_repeat.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* zeros_1_new = {self.zeros_1_new.__repr__()}'
		s += f'\n	* float_count = {self.float_count.__repr__()}'
		s += f'\n	* count_a = {self.count_a.__repr__()}'
		s += f'\n	* count_b = {self.count_b.__repr__()}'
		s += f'\n	* target_bone_count = {self.target_bone_count.__repr__()}'
		s += f'\n	* g = {self.g.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* extra_zeros_pc = {self.extra_zeros_pc.__repr__()}'
		s += f'\n	* pos_bone_min = {self.pos_bone_min.__repr__()}'
		s += f'\n	* pos_bone_max = {self.pos_bone_max.__repr__()}'
		s += f'\n	* ori_bone_min = {self.ori_bone_min.__repr__()}'
		s += f'\n	* ori_bone_max = {self.ori_bone_max.__repr__()}'
		s += f'\n	* scl_bone_min = {self.scl_bone_min.__repr__()}'
		s += f'\n	* scl_bone_max = {self.scl_bone_max.__repr__()}'
		s += f'\n	* pos_bone_count_related = {self.pos_bone_count_related.__repr__()}'
		s += f'\n	* ori_bone_count_related = {self.ori_bone_count_related.__repr__()}'
		s += f'\n	* scl_bone_count_related = {self.scl_bone_count_related.__repr__()}'
		s += f'\n	* zeros_end = {self.zeros_end.__repr__()}'
		s += f'\n	* zero_2_end = {self.zero_2_end.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
