import typing
from generated.formats.ms2.compound.BoundingBox import BoundingBox
from generated.formats.ms2.compound.Capsule import Capsule
from generated.formats.ms2.compound.Sphere import Sphere


class HitCheckEntry:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.type = 0
		self.unknown_2_a = 0
		self.unknown_2_b = 0

		# 16
		self.unknown_2_c = 0

		# 0
		self.unknown_2_d = 0

		# JWE: 564267, PZ: seen 17 and 22
		self.unknown_3 = 0

		# JWE: 46, PZ: same as above
		self.unknown_4 = 0

		# offset into joint names
		self.name_offset = 0
		self.collider = Sphere()
		self.collider = BoundingBox()
		self.collider = Capsule()

	def read(self, stream):

		self.io_start = stream.tell()
		self.type = stream.read_uint()
		self.unknown_2_a = stream.read_ubyte()
		self.unknown_2_b = stream.read_ubyte()
		self.unknown_2_c = stream.read_ubyte()
		self.unknown_2_d = stream.read_ubyte()
		self.unknown_3 = stream.read_uint()
		self.unknown_4 = stream.read_uint()
		self.name_offset = stream.read_uint()
		if self.type == 0:
			self.collider = stream.read_type(Sphere)
		if self.type == 1:
			self.collider = stream.read_type(BoundingBox)
		if self.type == 2:
			self.collider = stream.read_type(Capsule)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.type)
		stream.write_ubyte(self.unknown_2_a)
		stream.write_ubyte(self.unknown_2_b)
		stream.write_ubyte(self.unknown_2_c)
		stream.write_ubyte(self.unknown_2_d)
		stream.write_uint(self.unknown_3)
		stream.write_uint(self.unknown_4)
		stream.write_uint(self.name_offset)
		if self.type == 0:
			stream.write_type(self.collider)
		if self.type == 1:
			stream.write_type(self.collider)
		if self.type == 2:
			stream.write_type(self.collider)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'HitCheckEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* type = {self.type.__repr__()}'
		s += f'\n	* unknown_2_a = {self.unknown_2_a.__repr__()}'
		s += f'\n	* unknown_2_b = {self.unknown_2_b.__repr__()}'
		s += f'\n	* unknown_2_c = {self.unknown_2_c.__repr__()}'
		s += f'\n	* unknown_2_d = {self.unknown_2_d.__repr__()}'
		s += f'\n	* unknown_3 = {self.unknown_3.__repr__()}'
		s += f'\n	* unknown_4 = {self.unknown_4.__repr__()}'
		s += f'\n	* name_offset = {self.name_offset.__repr__()}'
		s += f'\n	* collider = {self.collider.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
