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

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.type = CollisionType(self.context, 0, None)

		# 0
		self.flag_0 = 0

		# JWE1: 16, PZ, JWE2: 0
		self.flag_1 = 0

		# JWE1: 564267, PZ: seen 17 and 22, JWE2: 34, 30
		self.flag_2 = 0

		# JWE1: 46, PZ: same as above, JWE2: 21, 27
		self.flag_3 = 0

		# ?
		self.zero_extra_pc_unk = 0

		# offset into joint names
		self.name_offset = 0
		self.collider = Sphere(self.context, 0, None)
		self.collider = BoundingBox(self.context, 0, None)
		self.collider = Capsule(self.context, 0, None)
		self.collider = Cylinder(self.context, 0, None)
		self.collider = ConvexHull(self.context, 0, None)
		self.collider = ConvexHull(self.context, 0, None)
		self.collider = MeshCollision(self.context, 0, None)

		# ?
		self.zero_extra_zt = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.type = CollisionType(self.context, 0, None)
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		if self.context.version < 47:
			self.zero_extra_pc_unk = 0
		self.name_offset = 0
		if self.type == 0:
			self.collider = Sphere(self.context, 0, None)
		if self.type == 1:
			self.collider = BoundingBox(self.context, 0, None)
		if self.type == 2:
			self.collider = Capsule(self.context, 0, None)
		if self.type == 3:
			self.collider = Cylinder(self.context, 0, None)
		if self.type == 7:
			self.collider = ConvexHull(self.context, 0, None)
		if self.type == 8:
			self.collider = ConvexHull(self.context, 0, None)
		if self.type == 10:
			self.collider = MeshCollision(self.context, 0, None)
		if self.context.version == 13:
			self.zero_extra_zt = 0

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
		instance.type = CollisionType.from_value(stream.read_uint())
		instance.flag_0 = stream.read_ushort()
		instance.flag_1 = stream.read_ushort()
		instance.flag_2 = stream.read_uint()
		instance.flag_3 = stream.read_uint()
		if instance.context.version < 47:
			instance.zero_extra_pc_unk = stream.read_uint()
		instance.name_offset = stream.read_uint()
		if instance.type == 0:
			instance.collider = Sphere.from_stream(stream, instance.context, 0, None)
		if instance.type == 1:
			instance.collider = BoundingBox.from_stream(stream, instance.context, 0, None)
		if instance.type == 2:
			instance.collider = Capsule.from_stream(stream, instance.context, 0, None)
		if instance.type == 3:
			instance.collider = Cylinder.from_stream(stream, instance.context, 0, None)
		if instance.type == 7:
			instance.collider = ConvexHull.from_stream(stream, instance.context, 0, None)
		if instance.type == 8:
			instance.collider = ConvexHull.from_stream(stream, instance.context, 0, None)
		if instance.type == 10:
			instance.collider = MeshCollision.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 13:
			instance.zero_extra_zt = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.type.value)
		stream.write_ushort(instance.flag_0)
		stream.write_ushort(instance.flag_1)
		stream.write_uint(instance.flag_2)
		stream.write_uint(instance.flag_3)
		if instance.context.version < 47:
			stream.write_uint(instance.zero_extra_pc_unk)
		stream.write_uint(instance.name_offset)
		if instance.type == 0:
			Sphere.to_stream(stream, instance.collider)
		if instance.type == 1:
			BoundingBox.to_stream(stream, instance.collider)
		if instance.type == 2:
			Capsule.to_stream(stream, instance.collider)
		if instance.type == 3:
			Cylinder.to_stream(stream, instance.collider)
		if instance.type == 7:
			ConvexHull.to_stream(stream, instance.collider)
		if instance.type == 8:
			ConvexHull.to_stream(stream, instance.collider)
		if instance.type == 10:
			MeshCollision.to_stream(stream, instance.collider)
		if instance.context.version == 13:
			stream.write_uint(instance.zero_extra_zt)

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
		return f'HitCheckEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* type = {self.type.__repr__()}'
		s += f'\n	* flag_0 = {self.flag_0.__repr__()}'
		s += f'\n	* flag_1 = {self.flag_1.__repr__()}'
		s += f'\n	* flag_2 = {self.flag_2.__repr__()}'
		s += f'\n	* flag_3 = {self.flag_3.__repr__()}'
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
