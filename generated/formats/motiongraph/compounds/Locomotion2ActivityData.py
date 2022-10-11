from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.compounds.Locomotion2BlendSpace import Locomotion2BlendSpace
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Locomotion2ActivityData(MemStruct):

	"""
	? bytes
	"""

	__name__ = 'Locomotion2ActivityData'

	_import_key = 'motiongraph.compounds.Locomotion2ActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.animation_count = 0
		self.flags = 0
		self.stopping_distance = 0.0
		self.strafe_turn_blend = 0.2
		self.turn_blend_limit = 1.0
		self.turn_speed_multiplier = 1.0
		self.flex_speed_multiplier = 1.0
		self.blend_space = Locomotion2BlendSpace(self.context, 0, None)
		self.data_streams_count = 0
		self.animations = ArrayPointer(self.context, self.animation_count, Locomotion2ActivityData._import_map["motiongraph.compounds.Locomotion2AnimationInfo"])
		self.output_prop_through_variable = Pointer(self.context, 0, ZString)
		self.speed_variable = Pointer(self.context, 0, ZString)
		self.orientation_variable = Pointer(self.context, 0, ZString)
		self.data_streams = ArrayPointer(self.context, self.data_streams_count, Locomotion2ActivityData._import_map["motiongraph.compounds.DataStreamResourceDataList"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('animation_count', Uint64, (0, None), (False, None), None),
		('animations', ArrayPointer, (None, None), (False, None), None),
		('flags', Uint, (0, None), (False, None), None),
		('stopping_distance', Float, (0, None), (False, 0.0), None),
		('strafe_turn_blend', Float, (0, None), (False, 0.2), None),
		('turn_blend_limit', Float, (0, None), (False, 1.0), None),
		('turn_speed_multiplier', Float, (0, None), (False, 1.0), None),
		('flex_speed_multiplier', Float, (0, None), (False, 1.0), None),
		('blend_space', Locomotion2BlendSpace, (0, None), (False, None), None),
		('output_prop_through_variable', Pointer, (0, ZString), (False, None), None),
		('speed_variable', Pointer, (0, ZString), (False, None), None),
		('orientation_variable', Pointer, (0, ZString), (False, None), None),
		('data_streams_count', Uint64, (0, None), (False, None), None),
		('data_streams', ArrayPointer, (None, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'animation_count', Uint64, (0, None), (False, None)
		yield 'animations', ArrayPointer, (instance.animation_count, Locomotion2ActivityData._import_map["motiongraph.compounds.Locomotion2AnimationInfo"]), (False, None)
		yield 'flags', Uint, (0, None), (False, None)
		yield 'stopping_distance', Float, (0, None), (False, 0.0)
		yield 'strafe_turn_blend', Float, (0, None), (False, 0.2)
		yield 'turn_blend_limit', Float, (0, None), (False, 1.0)
		yield 'turn_speed_multiplier', Float, (0, None), (False, 1.0)
		yield 'flex_speed_multiplier', Float, (0, None), (False, 1.0)
		yield 'blend_space', Locomotion2BlendSpace, (0, None), (False, None)
		yield 'output_prop_through_variable', Pointer, (0, ZString), (False, None)
		yield 'speed_variable', Pointer, (0, ZString), (False, None)
		yield 'orientation_variable', Pointer, (0, ZString), (False, None)
		yield 'data_streams_count', Uint64, (0, None), (False, None)
		yield 'data_streams', ArrayPointer, (instance.data_streams_count, Locomotion2ActivityData._import_map["motiongraph.compounds.DataStreamResourceDataList"]), (False, None)
