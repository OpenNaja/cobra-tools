import numpy
import typing
from generated.array import Array


class ManiInfo:

	"""
	288 bytes for JWE / PZ
	312 bytes for PC
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.duration = 0

		# likely
		self.frame_count = 0
		self.b = 0

		# rest
		self.zeros_0 = numpy.zeros((6), dtype='ushort')
		self.c_2 = 0
		self.c = 0
		self.name_count = 0

		# rest
		self.zeros_1 = numpy.zeros((3), dtype='ushort')
		self.e_2 = 0

		# always FF FF
		self.ff_1 = 0

		# always FF FF
		self.ff_2 = 0
		self.e = 0
		self.extra_pc = numpy.zeros((5), dtype='ushort')
		self.g = 0

		# rest 228 bytes
		self.zeros_2 = numpy.zeros((57), dtype='uint')

		# rest 14 bytes
		self.extra_zeros_pc = numpy.zeros((7), dtype='ushort')
		self.i = 0
		self.j = 0

		# always FF
		self.ff = 0
		self.k = 0
		self.l = 0
		self.zeros_end = numpy.zeros((3), dtype='ushort')

	def read(self, stream):

		self.io_start = stream.tell()
		self.duration = stream.read_float()
		self.frame_count = stream.read_uint()
		self.b = stream.read_uint()
		self.zeros_0 = stream.read_ushorts((6))
		self.c_2 = stream.read_ushort()
		self.c = stream.read_ushort()
		self.name_count = stream.read_ushort()
		self.zeros_1 = stream.read_ushorts((3))
		self.e_2 = stream.read_ushort()
		self.ff_1 = stream.read_ubyte()
		self.ff_2 = stream.read_ubyte()
		self.e = stream.read_ushort()
		if stream.version == 18:
			self.extra_pc = stream.read_ushorts((5))
		self.g = stream.read_ushort()
		self.zeros_2 = stream.read_uints((57))
		if stream.version == 18:
			self.extra_zeros_pc = stream.read_ushorts((7))
		self.i = stream.read_ushort()
		self.j = stream.read_ushort()
		self.ff = stream.read_ushort()
		self.k = stream.read_ushort()
		self.l = stream.read_ushort()
		self.zeros_end = stream.read_ushorts((3))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_float(self.duration)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.b)
		stream.write_ushorts(self.zeros_0)
		stream.write_ushort(self.c_2)
		stream.write_ushort(self.c)
		stream.write_ushort(self.name_count)
		stream.write_ushorts(self.zeros_1)
		stream.write_ushort(self.e_2)
		stream.write_ubyte(self.ff_1)
		stream.write_ubyte(self.ff_2)
		stream.write_ushort(self.e)
		if stream.version == 18:
			stream.write_ushorts(self.extra_pc)
		stream.write_ushort(self.g)
		stream.write_uints(self.zeros_2)
		if stream.version == 18:
			stream.write_ushorts(self.extra_zeros_pc)
		stream.write_ushort(self.i)
		stream.write_ushort(self.j)
		stream.write_ushort(self.ff)
		stream.write_ushort(self.k)
		stream.write_ushort(self.l)
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
		s += f'\n	* c_2 = {self.c_2.__repr__()}'
		s += f'\n	* c = {self.c.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* e_2 = {self.e_2.__repr__()}'
		s += f'\n	* ff_1 = {self.ff_1.__repr__()}'
		s += f'\n	* ff_2 = {self.ff_2.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* extra_pc = {self.extra_pc.__repr__()}'
		s += f'\n	* g = {self.g.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* extra_zeros_pc = {self.extra_zeros_pc.__repr__()}'
		s += f'\n	* i = {self.i.__repr__()}'
		s += f'\n	* j = {self.j.__repr__()}'
		s += f'\n	* ff = {self.ff.__repr__()}'
		s += f'\n	* k = {self.k.__repr__()}'
		s += f'\n	* l = {self.l.__repr__()}'
		s += f'\n	* zeros_end = {self.zeros_end.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
