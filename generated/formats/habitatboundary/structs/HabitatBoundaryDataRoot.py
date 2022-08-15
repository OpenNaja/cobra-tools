import generated.formats.base.basic
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.habitatboundary.structs.HbOffsets import HbOffsets
from generated.formats.habitatboundary.structs.HbUiOptions import HbUiOptions
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class HabitatBoundaryDataRoot(MemStruct):

	"""
	224 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 3 for everything but null barrier which is 0
		self.u_1 = 0
		self.u_2 = 0.0

		# 0 for everything but wood logs barrier which is 1
		self.u_3 = 0
		self.ui_options = HbUiOptions(self.context, 0, None)
		self.u_4 = 0.0
		self.u_5 = 0.0
		self.offsets = HbOffsets(self.context, 0, None)

		# Posts of N Level can only use Walls of less than N Level
		self.wall_replace_level = 0

		# 0 = Glass, 1 = Null, 3 = Solid Opaques (Brick, Concrete), 4 = 1-Way Glass, 5 = Wire Fences, 7 = Electrified Wire Fence
		self.type = 0
		self.padding = 0
		self.prefab = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_top = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_cap_top = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_bottom = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_unk_2 = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_unk_3 = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_unk_4 = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_door_cap_side = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_door_cap_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_door_cap_underside = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_data = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion_pile = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_ground = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_1_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_10_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post_cap = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.u_1 = 0
		self.u_2 = 0.0
		self.u_3 = 0
		self.ui_options = HbUiOptions(self.context, 0, None)
		self.u_4 = 0.0
		self.u_5 = 0.0
		self.offsets = HbOffsets(self.context, 0, None)
		self.wall_replace_level = 0
		self.type = 0
		self.padding = 0
		self.prefab = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_top = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_cap_top = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_bottom = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_unk_2 = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_unk_3 = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_unk_4 = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_door_cap_side = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_door_cap_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_door_cap_underside = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_data = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion_pile = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_ground = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_1_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_10_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post_cap = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.prefab = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_end = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_top = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_cap_top = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_bottom = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_unk_2 = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_unk_3 = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_unk_4 = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_door_cap_side = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_door_cap_end = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_door_cap_underside = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.climb_proof_data = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_post = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_extrusion = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_extrusion_pile = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_ground = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_1_m = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_10_m = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.post = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.post_cap = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_2 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_3 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.ui_options = HbUiOptions.from_stream(stream, instance.context, 0, None)
		instance.u_4 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_5 = Float.from_stream(stream, instance.context, 0, None)
		instance.offsets = HbOffsets.from_stream(stream, instance.context, 0, None)
		instance.wall_replace_level = Byte.from_stream(stream, instance.context, 0, None)
		instance.type = Byte.from_stream(stream, instance.context, 0, None)
		instance.padding = Ushort.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.prefab, int):
			instance.prefab.arg = 0
		if not isinstance(instance.walls_extrusion, int):
			instance.walls_extrusion.arg = 0
		if not isinstance(instance.walls_extrusion_end, int):
			instance.walls_extrusion_end.arg = 0
		if not isinstance(instance.walls_extrusion_top, int):
			instance.walls_extrusion_top.arg = 0
		if not isinstance(instance.walls_extrusion_cap_top, int):
			instance.walls_extrusion_cap_top.arg = 0
		if not isinstance(instance.walls_extrusion_bottom, int):
			instance.walls_extrusion_bottom.arg = 0
		if not isinstance(instance.walls_unk_2, int):
			instance.walls_unk_2.arg = 0
		if not isinstance(instance.walls_unk_3, int):
			instance.walls_unk_3.arg = 0
		if not isinstance(instance.walls_unk_4, int):
			instance.walls_unk_4.arg = 0
		if not isinstance(instance.walls_extrusion_door_cap_side, int):
			instance.walls_extrusion_door_cap_side.arg = 0
		if not isinstance(instance.walls_extrusion_door_cap_end, int):
			instance.walls_extrusion_door_cap_end.arg = 0
		if not isinstance(instance.walls_extrusion_door_cap_underside, int):
			instance.walls_extrusion_door_cap_underside.arg = 0
		if not isinstance(instance.climb_proof_data, int):
			instance.climb_proof_data.arg = 0
		if not isinstance(instance.broken_post, int):
			instance.broken_post.arg = 0
		if not isinstance(instance.broken_extrusion, int):
			instance.broken_extrusion.arg = 0
		if not isinstance(instance.broken_extrusion_pile, int):
			instance.broken_extrusion_pile.arg = 0
		if not isinstance(instance.broken_ground, int):
			instance.broken_ground.arg = 0
		if not isinstance(instance.broken_1_m, int):
			instance.broken_1_m.arg = 0
		if not isinstance(instance.broken_10_m, int):
			instance.broken_10_m.arg = 0
		if not isinstance(instance.post, int):
			instance.post.arg = 0
		if not isinstance(instance.post_cap, int):
			instance.post_cap.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.prefab)
		Pointer.to_stream(stream, instance.walls_extrusion)
		Pointer.to_stream(stream, instance.walls_extrusion_end)
		Pointer.to_stream(stream, instance.walls_extrusion_top)
		Pointer.to_stream(stream, instance.walls_extrusion_cap_top)
		Pointer.to_stream(stream, instance.walls_extrusion_bottom)
		Pointer.to_stream(stream, instance.walls_unk_2)
		Pointer.to_stream(stream, instance.walls_unk_3)
		Pointer.to_stream(stream, instance.walls_unk_4)
		Pointer.to_stream(stream, instance.walls_extrusion_door_cap_side)
		Pointer.to_stream(stream, instance.walls_extrusion_door_cap_end)
		Pointer.to_stream(stream, instance.walls_extrusion_door_cap_underside)
		Pointer.to_stream(stream, instance.climb_proof_data)
		Pointer.to_stream(stream, instance.broken_post)
		Pointer.to_stream(stream, instance.broken_extrusion)
		Pointer.to_stream(stream, instance.broken_extrusion_pile)
		Pointer.to_stream(stream, instance.broken_ground)
		Pointer.to_stream(stream, instance.broken_1_m)
		Pointer.to_stream(stream, instance.broken_10_m)
		Pointer.to_stream(stream, instance.post)
		Pointer.to_stream(stream, instance.post_cap)
		Uint.to_stream(stream, instance.u_1)
		Float.to_stream(stream, instance.u_2)
		Ushort.to_stream(stream, instance.u_3)
		HbUiOptions.to_stream(stream, instance.ui_options)
		Float.to_stream(stream, instance.u_4)
		Float.to_stream(stream, instance.u_5)
		HbOffsets.to_stream(stream, instance.offsets)
		Byte.to_stream(stream, instance.wall_replace_level)
		Byte.to_stream(stream, instance.type)
		Ushort.to_stream(stream, instance.padding)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'prefab', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion_end', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion_top', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion_cap_top', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion_bottom', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_unk_2', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_unk_3', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_unk_4', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion_door_cap_side', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion_door_cap_end', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'walls_extrusion_door_cap_underside', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'climb_proof_data', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'broken_post', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'broken_extrusion', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'broken_extrusion_pile', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'broken_ground', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'broken_1_m', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'broken_10_m', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'post', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'post_cap', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'u_1', Uint, (0, None), (False, None)
		yield 'u_2', Float, (0, None), (False, None)
		yield 'u_3', Ushort, (0, None), (False, None)
		yield 'ui_options', HbUiOptions, (0, None), (False, None)
		yield 'u_4', Float, (0, None), (False, None)
		yield 'u_5', Float, (0, None), (False, None)
		yield 'offsets', HbOffsets, (0, None), (False, None)
		yield 'wall_replace_level', Byte, (0, None), (False, None)
		yield 'type', Byte, (0, None), (False, None)
		yield 'padding', Ushort, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'HabitatBoundaryDataRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* prefab = {self.fmt_member(self.prefab, indent+1)}'
		s += f'\n	* walls_extrusion = {self.fmt_member(self.walls_extrusion, indent+1)}'
		s += f'\n	* walls_extrusion_end = {self.fmt_member(self.walls_extrusion_end, indent+1)}'
		s += f'\n	* walls_extrusion_top = {self.fmt_member(self.walls_extrusion_top, indent+1)}'
		s += f'\n	* walls_extrusion_cap_top = {self.fmt_member(self.walls_extrusion_cap_top, indent+1)}'
		s += f'\n	* walls_extrusion_bottom = {self.fmt_member(self.walls_extrusion_bottom, indent+1)}'
		s += f'\n	* walls_unk_2 = {self.fmt_member(self.walls_unk_2, indent+1)}'
		s += f'\n	* walls_unk_3 = {self.fmt_member(self.walls_unk_3, indent+1)}'
		s += f'\n	* walls_unk_4 = {self.fmt_member(self.walls_unk_4, indent+1)}'
		s += f'\n	* walls_extrusion_door_cap_side = {self.fmt_member(self.walls_extrusion_door_cap_side, indent+1)}'
		s += f'\n	* walls_extrusion_door_cap_end = {self.fmt_member(self.walls_extrusion_door_cap_end, indent+1)}'
		s += f'\n	* walls_extrusion_door_cap_underside = {self.fmt_member(self.walls_extrusion_door_cap_underside, indent+1)}'
		s += f'\n	* climb_proof_data = {self.fmt_member(self.climb_proof_data, indent+1)}'
		s += f'\n	* broken_post = {self.fmt_member(self.broken_post, indent+1)}'
		s += f'\n	* broken_extrusion = {self.fmt_member(self.broken_extrusion, indent+1)}'
		s += f'\n	* broken_extrusion_pile = {self.fmt_member(self.broken_extrusion_pile, indent+1)}'
		s += f'\n	* broken_ground = {self.fmt_member(self.broken_ground, indent+1)}'
		s += f'\n	* broken_1_m = {self.fmt_member(self.broken_1_m, indent+1)}'
		s += f'\n	* broken_10_m = {self.fmt_member(self.broken_10_m, indent+1)}'
		s += f'\n	* post = {self.fmt_member(self.post, indent+1)}'
		s += f'\n	* post_cap = {self.fmt_member(self.post_cap, indent+1)}'
		s += f'\n	* u_1 = {self.fmt_member(self.u_1, indent+1)}'
		s += f'\n	* u_2 = {self.fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_3 = {self.fmt_member(self.u_3, indent+1)}'
		s += f'\n	* ui_options = {self.fmt_member(self.ui_options, indent+1)}'
		s += f'\n	* u_4 = {self.fmt_member(self.u_4, indent+1)}'
		s += f'\n	* u_5 = {self.fmt_member(self.u_5, indent+1)}'
		s += f'\n	* offsets = {self.fmt_member(self.offsets, indent+1)}'
		s += f'\n	* wall_replace_level = {self.fmt_member(self.wall_replace_level, indent+1)}'
		s += f'\n	* type = {self.fmt_member(self.type, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
