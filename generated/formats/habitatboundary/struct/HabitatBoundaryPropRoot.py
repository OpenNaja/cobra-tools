from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.habitatboundary.struct.HbDoorCutout import HbDoorCutout
from generated.formats.habitatboundary.struct.HbPostPos import HbPostPos
from generated.formats.habitatboundary.struct.HbPropPhysics import HbPropPhysics
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class HabitatBoundaryPropRoot(MemStruct):

	"""
	144 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 0 = Habitat, 1 = Ride, 2 = Guest
		self.type = 0
		self.u_1 = 0
		self.is_guest = 0
		self.post_position = 0
		self.u_2 = 0
		self.door_physics = 0
		self.path_physics = 0
		self.door_cutout = 0
		self.small = 0
		self.height = 0
		self.prefab = 0
		self.post = 0
		self.wall = 0
		self.path_join_part = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.type = 0
		self.u_1 = 0
		self.is_guest = 0
		self.post_position = HbPostPos(self.context, 0, None)
		self.u_2 = 0.0
		self.door_physics = HbPropPhysics(self.context, 0, None)
		self.path_physics = HbPropPhysics(self.context, 0, None)
		self.door_cutout = HbDoorCutout(self.context, 0, None)
		self.small = 0
		self.height = 0.0
		self.prefab = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.wall = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.path_join_part = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		super().read_fields(stream, instance)
		instance.type = stream.read_uint64()
		instance.prefab = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_1 = stream.read_uint64()
		instance.post = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.wall = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.is_guest = stream.read_uint()
		instance.post_position = HbPostPos.from_stream(stream, instance.context, 0, None)
		instance.u_2 = stream.read_float()
		instance.door_physics = HbPropPhysics.from_stream(stream, instance.context, 0, None)
		instance.path_physics = HbPropPhysics.from_stream(stream, instance.context, 0, None)
		instance.path_join_part = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.door_cutout = HbDoorCutout.from_stream(stream, instance.context, 0, None)
		instance.small = stream.read_uint()
		instance.height = stream.read_float()
		instance.prefab.arg = 0
		instance.post.arg = 0
		instance.wall.arg = 0
		instance.path_join_part.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.type)
		Pointer.to_stream(stream, instance.prefab)
		stream.write_uint64(instance.u_1)
		Pointer.to_stream(stream, instance.post)
		Pointer.to_stream(stream, instance.wall)
		stream.write_uint(instance.is_guest)
		HbPostPos.to_stream(stream, instance.post_position)
		stream.write_float(instance.u_2)
		HbPropPhysics.to_stream(stream, instance.door_physics)
		HbPropPhysics.to_stream(stream, instance.path_physics)
		Pointer.to_stream(stream, instance.path_join_part)
		HbDoorCutout.to_stream(stream, instance.door_cutout)
		stream.write_uint(instance.small)
		stream.write_float(instance.height)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('type', Uint64, (0, None))
		yield ('prefab', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('u_1', Uint64, (0, None))
		yield ('post', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('wall', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('is_guest', Uint, (0, None))
		yield ('post_position', HbPostPos, (0, None))
		yield ('u_2', Float, (0, None))
		yield ('door_physics', HbPropPhysics, (0, None))
		yield ('path_physics', HbPropPhysics, (0, None))
		yield ('path_join_part', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('door_cutout', HbDoorCutout, (0, None))
		yield ('small', Uint, (0, None))
		yield ('height', Float, (0, None))

	def get_info_str(self, indent=0):
		return f'HabitatBoundaryPropRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* type = {fmt_member(self.type, indent+1)}'
		s += f'\n	* prefab = {fmt_member(self.prefab, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* post = {fmt_member(self.post, indent+1)}'
		s += f'\n	* wall = {fmt_member(self.wall, indent+1)}'
		s += f'\n	* is_guest = {fmt_member(self.is_guest, indent+1)}'
		s += f'\n	* post_position = {fmt_member(self.post_position, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* door_physics = {fmt_member(self.door_physics, indent+1)}'
		s += f'\n	* path_physics = {fmt_member(self.path_physics, indent+1)}'
		s += f'\n	* path_join_part = {fmt_member(self.path_join_part, indent+1)}'
		s += f'\n	* door_cutout = {fmt_member(self.door_cutout, indent+1)}'
		s += f'\n	* small = {fmt_member(self.small, indent+1)}'
		s += f'\n	* height = {fmt_member(self.height, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
