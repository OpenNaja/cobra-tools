from generated.formats.base.basic import Byte
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.habitatboundary.structs.HbOffsets import HbOffsets
from generated.formats.habitatboundary.structs.HbUiOptions import HbUiOptions
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class HabitatBoundaryDataRoot(MemStruct):

	"""
	224 bytes
	"""

	__name__ = 'HabitatBoundaryDataRoot'

	_import_key = 'habitatboundary.structs.HabitatBoundaryDataRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 3 for everything but null barrier which is 0
		self.u_1 = 3
		self.u_2 = 0.0

		# 0 for everything but wood logs barrier which is 1
		self.u_3 = 0
		self.ui_options = HbUiOptions(self.context, 0, None)
		self.u_4 = 1.5
		self.u_5 = 2.5
		self.offsets = HbOffsets(self.context, 0, None)

		# Posts of N Level can only use Walls of less than N Level
		self.wall_replace_level = 0

		# 0 = Glass, 1 = Null, 3 = Solid Opaques (Brick, Concrete), 4 = 1-Way Glass, 5 = Wire Fences, 7 = Electrified Wire Fence
		self.type = 0
		self.padding = 0
		self.prefab = Pointer(self.context, 0, ZString)
		self.walls_extrusion = Pointer(self.context, 0, ZString)
		self.walls_extrusion_end = Pointer(self.context, 0, ZString)
		self.walls_extrusion_top = Pointer(self.context, 0, ZString)
		self.walls_extrusion_cap_top = Pointer(self.context, 0, ZString)
		self.walls_extrusion_bottom = Pointer(self.context, 0, ZString)
		self.walls_unk_2 = Pointer(self.context, 0, ZString)
		self.walls_unk_3 = Pointer(self.context, 0, ZString)
		self.walls_unk_4 = Pointer(self.context, 0, ZString)
		self.walls_extrusion_door_cap_side = Pointer(self.context, 0, ZString)
		self.walls_extrusion_door_cap_end = Pointer(self.context, 0, ZString)
		self.walls_extrusion_door_cap_underside = Pointer(self.context, 0, ZString)
		self.climb_proof_data = Pointer(self.context, 0, ZString)
		self.broken_post = Pointer(self.context, 0, ZString)
		self.broken_extrusion = Pointer(self.context, 0, ZString)
		self.broken_extrusion_pile = Pointer(self.context, 0, ZString)
		self.broken_ground = Pointer(self.context, 0, ZString)
		self.broken_1_m = Pointer(self.context, 0, ZString)
		self.broken_10_m = Pointer(self.context, 0, ZString)
		self.post = Pointer(self.context, 0, ZString)
		self.post_cap = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('prefab', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion_end', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion_top', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion_cap_top', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion_bottom', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_unk_2', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_unk_3', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_unk_4', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion_door_cap_side', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion_door_cap_end', Pointer, (0, ZString), (False, None), (None, None))
		yield ('walls_extrusion_door_cap_underside', Pointer, (0, ZString), (False, None), (None, None))
		yield ('climb_proof_data', Pointer, (0, ZString), (False, None), (None, None))
		yield ('broken_post', Pointer, (0, ZString), (False, None), (None, None))
		yield ('broken_extrusion', Pointer, (0, ZString), (False, None), (None, None))
		yield ('broken_extrusion_pile', Pointer, (0, ZString), (False, None), (None, None))
		yield ('broken_ground', Pointer, (0, ZString), (False, None), (None, None))
		yield ('broken_1_m', Pointer, (0, ZString), (False, None), (None, None))
		yield ('broken_10_m', Pointer, (0, ZString), (False, None), (None, None))
		yield ('post', Pointer, (0, ZString), (False, None), (None, None))
		yield ('post_cap', Pointer, (0, ZString), (False, None), (None, None))
		yield ('u_1', Uint, (0, None), (False, 3), (None, None))
		yield ('u_2', Float, (0, None), (False, None), (None, None))
		yield ('u_3', Ushort, (0, None), (False, 0), (None, None))
		yield ('ui_options', HbUiOptions, (0, None), (False, None), (None, None))
		yield ('u_4', Float, (0, None), (False, 1.5), (None, None))
		yield ('u_5', Float, (0, None), (False, 2.5), (None, None))
		yield ('offsets', HbOffsets, (0, None), (False, None), (None, None))
		yield ('wall_replace_level', Byte, (0, None), (False, None), (None, None))
		yield ('type', Byte, (0, None), (False, None), (None, None))
		yield ('padding', Ushort, (0, None), (True, 0), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'prefab', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion_end', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion_top', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion_cap_top', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion_bottom', Pointer, (0, ZString), (False, None)
		yield 'walls_unk_2', Pointer, (0, ZString), (False, None)
		yield 'walls_unk_3', Pointer, (0, ZString), (False, None)
		yield 'walls_unk_4', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion_door_cap_side', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion_door_cap_end', Pointer, (0, ZString), (False, None)
		yield 'walls_extrusion_door_cap_underside', Pointer, (0, ZString), (False, None)
		yield 'climb_proof_data', Pointer, (0, ZString), (False, None)
		yield 'broken_post', Pointer, (0, ZString), (False, None)
		yield 'broken_extrusion', Pointer, (0, ZString), (False, None)
		yield 'broken_extrusion_pile', Pointer, (0, ZString), (False, None)
		yield 'broken_ground', Pointer, (0, ZString), (False, None)
		yield 'broken_1_m', Pointer, (0, ZString), (False, None)
		yield 'broken_10_m', Pointer, (0, ZString), (False, None)
		yield 'post', Pointer, (0, ZString), (False, None)
		yield 'post_cap', Pointer, (0, ZString), (False, None)
		yield 'u_1', Uint, (0, None), (False, 3)
		yield 'u_2', Float, (0, None), (False, None)
		yield 'u_3', Ushort, (0, None), (False, 0)
		yield 'ui_options', HbUiOptions, (0, None), (False, None)
		yield 'u_4', Float, (0, None), (False, 1.5)
		yield 'u_5', Float, (0, None), (False, 2.5)
		yield 'offsets', HbOffsets, (0, None), (False, None)
		yield 'wall_replace_level', Byte, (0, None), (False, None)
		yield 'type', Byte, (0, None), (False, None)
		yield 'padding', Ushort, (0, None), (True, 0)
