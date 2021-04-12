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
		self.zeros_start = numpy.zeros((5), dtype='ushort')
		self.duration = 0

		# likely
		self.frame_count = 0
		self.b = 0

		# rest
		self.zeros_0 = numpy.zeros((7), dtype='ushort')
		self.c = 0
		self.name_count = 0

		# rest
		self.zeros_1 = numpy.zeros((4), dtype='ushort')
		self.e = 0
		self.extra_pc = numpy.zeros((5), dtype='ushort')

		# always FF FF
		self.ffff = 0
		self.g = 0

		# rest 228 bytes
		self.zeros_2 = numpy.zeros((57), dtype='uint')

		# rest 14 bytes
		self.extra_zeros_pc = numpy.zeros((7), dtype='ushort')
		self.i = 0
		self.j = 0

		# always FF
		self.ff = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros_start = stream.read_ushorts((5))
		self.duration = stream.read_float()
		self.frame_count = stream.read_uint()
		self.b = stream.read_uint()
		self.zeros_0 = stream.read_ushorts((7))
		self.c = stream.read_ushort()
		self.name_count = stream.read_ushort()
		self.zeros_1 = stream.read_ushorts((4))
		self.e = stream.read_ushort()
		if stream.version == 18:
			self.extra_pc = stream.read_ushorts((5))
		self.ffff = stream.read_ushort()
		self.g = stream.read_ushort()
		self.zeros_2 = stream.read_uints((57))
		if stream.version == 18:
			self.extra_zeros_pc = stream.read_ushorts((7))
		self.i = stream.read_ushort()
		self.j = stream.read_ushort()
		self.ff = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushorts(self.zeros_start)
		stream.write_float(self.duration)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.b)
		stream.write_ushorts(self.zeros_0)
		stream.write_ushort(self.c)
		stream.write_ushort(self.name_count)
		stream.write_ushorts(self.zeros_1)
		stream.write_ushort(self.e)
		if stream.version == 18:
			stream.write_ushorts(self.extra_pc)
		stream.write_ushort(self.ffff)
		stream.write_ushort(self.g)
		stream.write_uints(self.zeros_2)
		if stream.version == 18:
			stream.write_ushorts(self.extra_zeros_pc)
		stream.write_ushort(self.i)
		stream.write_ushort(self.j)
		stream.write_ushort(self.ff)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros_start = {self.zeros_start.__repr__()}'
		s += f'\n	* duration = {self.duration.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* c = {self.c.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* extra_pc = {self.extra_pc.__repr__()}'
		s += f'\n	* ffff = {self.ffff.__repr__()}'
		s += f'\n	* g = {self.g.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* extra_zeros_pc = {self.extra_zeros_pc.__repr__()}'
		s += f'\n	* i = {self.i.__repr__()}'
		s += f'\n	* j = {self.j.__repr__()}'
		s += f'\n	* ff = {self.ff.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
