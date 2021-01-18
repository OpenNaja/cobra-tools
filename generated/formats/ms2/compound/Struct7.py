import typing
from generated.array import Array
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry


class Struct7:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.count_7 = 0

		# 0
		self.unknown_2 = 0

		# 0 or 1
		self.unknown_3_pz = 0

		# 0 or 1
		self.unknown_f_pz = 0

		# 0
		self.unknown_4_pz = 0

		# 60 bytes per entry
		self.unknown_list = Array()

		# align list to multiples of 8
		self.padding = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.count_7 = stream.read_uint64()
		self.unknown_2 = stream.read_uint64()
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.unknown_3_pz = stream.read_uint()
			self.unknown_f_pz = stream.read_float()
			self.unknown_4_pz = stream.read_uint64()
		self.unknown_list.read(stream, NasutoJointEntry, self.count_7, None)
		self.padding = stream.read_ubytes(((8 - ((self.count_7 * 60) % 8)) % 8))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.count_7)
		stream.write_uint64(self.unknown_2)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			stream.write_uint(self.unknown_3_pz)
			stream.write_float(self.unknown_f_pz)
			stream.write_uint64(self.unknown_4_pz)
		self.unknown_list.write(stream, NasutoJointEntry, self.count_7, None)
		stream.write_ubytes(self.padding)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Struct7 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* unknown_2 = {self.unknown_2.__repr__()}'
		s += f'\n	* unknown_3_pz = {self.unknown_3_pz.__repr__()}'
		s += f'\n	* unknown_f_pz = {self.unknown_f_pz.__repr__()}'
		s += f'\n	* unknown_4_pz = {self.unknown_4_pz.__repr__()}'
		s += f'\n	* unknown_list = {self.unknown_list.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
