from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.habitatboundary.structs.HbDoorCutout import HbDoorCutout
from generated.formats.habitatboundary.structs.HbPostPos import HbPostPos
from generated.formats.habitatboundary.structs.HbPropPhysics import HbPropPhysics
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class HabitatBoundaryPropRoot(MemStruct):

	"""
	144 bytes
	"""

	__name__ = 'HabitatBoundaryPropRoot'

	_import_key = 'habitatboundary.structs.HabitatBoundaryPropRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 0 = Habitat, 1 = Ride, 2 = Guest
		self.type = 0
		self.u_1 = 0
		self.is_guest = 0
		self.post_position = HbPostPos(self.context, 0, None)
		self.u_2 = 0.0
		self.door_physics = HbPropPhysics(self.context, 0, None)
		self.path_physics = HbPropPhysics(self.context, 0, None)
		self.door_cutout = HbDoorCutout(self.context, 0, None)
		self.small = 0
		self.height = 2.0
		self.prefab = Pointer(self.context, 0, ZString)
		self.post = Pointer(self.context, 0, ZString)
		self.wall = Pointer(self.context, 0, ZString)
		self.path_join_part = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('type', Uint64, (0, None), (False, None), None)
		yield ('prefab', Pointer, (0, ZString), (False, None), None)
		yield ('u_1', Uint64, (0, None), (False, None), None)
		yield ('post', Pointer, (0, ZString), (False, None), None)
		yield ('wall', Pointer, (0, ZString), (False, None), None)
		yield ('is_guest', Uint, (0, None), (False, None), None)
		yield ('post_position', HbPostPos, (0, None), (False, None), None)
		yield ('u_2', Float, (0, None), (False, None), None)
		yield ('door_physics', HbPropPhysics, (0, None), (False, None), None)
		yield ('path_physics', HbPropPhysics, (0, None), (False, None), None)
		yield ('path_join_part', Pointer, (0, ZString), (False, None), None)
		yield ('door_cutout', HbDoorCutout, (0, None), (False, None), None)
		yield ('small', Uint, (0, None), (False, None), None)
		yield ('height', Float, (0, None), (False, 2.0), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'type', Uint64, (0, None), (False, None)
		yield 'prefab', Pointer, (0, ZString), (False, None)
		yield 'u_1', Uint64, (0, None), (False, None)
		yield 'post', Pointer, (0, ZString), (False, None)
		yield 'wall', Pointer, (0, ZString), (False, None)
		yield 'is_guest', Uint, (0, None), (False, None)
		yield 'post_position', HbPostPos, (0, None), (False, None)
		yield 'u_2', Float, (0, None), (False, None)
		yield 'door_physics', HbPropPhysics, (0, None), (False, None)
		yield 'path_physics', HbPropPhysics, (0, None), (False, None)
		yield 'path_join_part', Pointer, (0, ZString), (False, None)
		yield 'door_cutout', HbDoorCutout, (0, None), (False, None)
		yield 'small', Uint, (0, None), (False, None)
		yield 'height', Float, (0, None), (False, 2.0)


HabitatBoundaryPropRoot.init_attributes()
