from generated.context import ContextReference
from generated.formats.ms2.compound.BoundingBox import BoundingBox
from generated.formats.ms2.compound.Capsule import Capsule
from generated.formats.ms2.compound.ConvexHull import ConvexHull
from generated.formats.ms2.compound.Cylinder import Cylinder
from generated.formats.ms2.compound.MeshCollision import MeshCollision
from generated.formats.ms2.compound.Sphere import Sphere
from generated.formats.ms2.enum.CollisionType import CollisionType


class HitCheckEntry:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.type = CollisionType()
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
		self.zero_extra_pc_unk = 0

		# offset into joint names
		self.name_offset = 0
		self.collider = Sphere(self.context, None, None)
		self.collider = BoundingBox(self.context, None, None)
		self.collider = Capsule(self.context, None, None)
		self.collider = Cylinder(self.context, None, None)
		self.collider = ConvexHull(self.context, None, None)
		self.collider = ConvexHull(self.context, None, None)
		self.collider = MeshCollision(self.context, None, None)
		self.zero_extra_zt = 0
		self.set_defaults()

	def set_defaults(self):
		self.type = CollisionType()
		self.unknown_2_a = 0
		self.unknown_2_b = 0
		self.unknown_2_c = 0
		self.unknown_2_d = 0
		self.unknown_3 = 0
		self.unknown_4 = 0
		if self.context.version < 47:
			self.zero_extra_pc_unk = 0
		self.name_offset = 0
		if self.type == 0:
			self.collider = Sphere(self.context, None, None)
		if self.type == 1:
			self.collider = BoundingBox(self.context, None, None)
		if self.type == 2:
			self.collider = Capsule(self.context, None, None)
		if self.type == 3:
			self.collider = Cylinder(self.context, None, None)
		if self.type == 7:
			self.collider = ConvexHull(self.context, None, None)
		if self.type == 8:
			self.collider = ConvexHull(self.context, None, None)
		if self.type == 10:
			self.collider = MeshCollision(self.context, None, None)
		if self.context.version == 13:
			self.zero_extra_zt = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.type = CollisionType(stream.read_uint())
		self.unknown_2_a = stream.read_ubyte()
		self.unknown_2_b = stream.read_ubyte()
		self.unknown_2_c = stream.read_ubyte()
		self.unknown_2_d = stream.read_ubyte()
		self.unknown_3 = stream.read_uint()
		self.unknown_4 = stream.read_uint()
		if self.context.version < 47:
			self.zero_extra_pc_unk = stream.read_uint()
		self.name_offset = stream.read_uint()
		if self.type == 0:
			self.collider = stream.read_type(Sphere, (self.context, None, None))
		if self.type == 1:
			self.collider = stream.read_type(BoundingBox, (self.context, None, None))
		if self.type == 2:
			self.collider = stream.read_type(Capsule, (self.context, None, None))
		if self.type == 3:
			self.collider = stream.read_type(Cylinder, (self.context, None, None))
		if self.type == 7:
			self.collider = stream.read_type(ConvexHull, (self.context, None, None))
		if self.type == 8:
			self.collider = stream.read_type(ConvexHull, (self.context, None, None))
		if self.type == 10:
			self.collider = stream.read_type(MeshCollision, (self.context, None, None))
		if self.context.version == 13:
			self.zero_extra_zt = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.type.value)
		stream.write_ubyte(self.unknown_2_a)
		stream.write_ubyte(self.unknown_2_b)
		stream.write_ubyte(self.unknown_2_c)
		stream.write_ubyte(self.unknown_2_d)
		stream.write_uint(self.unknown_3)
		stream.write_uint(self.unknown_4)
		if self.context.version < 47:
			stream.write_uint(self.zero_extra_pc_unk)
		stream.write_uint(self.name_offset)
		if self.type == 0:
			stream.write_type(self.collider)
		if self.type == 1:
			stream.write_type(self.collider)
		if self.type == 2:
			stream.write_type(self.collider)
		if self.type == 3:
			stream.write_type(self.collider)
		if self.type == 7:
			stream.write_type(self.collider)
		if self.type == 8:
			stream.write_type(self.collider)
		if self.type == 10:
			stream.write_type(self.collider)
		if self.context.version == 13:
			stream.write_uint(self.zero_extra_zt)

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
		s += f'\n	* zero_extra_pc_unk = {self.zero_extra_pc_unk.__repr__()}'
		s += f'\n	* name_offset = {self.name_offset.__repr__()}'
		s += f'\n	* collider = {self.collider.__repr__()}'
		s += f'\n	* zero_extra_zt = {self.zero_extra_zt.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
