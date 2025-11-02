from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Locomotion2ActivityData(MemStruct):

	"""
	differs between games, not mime version
	PZ 88 bytes
	JWE2 112 bytes
	"""

	__name__ = 'Locomotion2ActivityData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.animation_count = name_type_map['Uint64'](self.context, 0, None)

		# Locomotion2Flags
		self.flags = name_type_map['Uint'](self.context, 0, None)
		self.stopping_distance = name_type_map['Float'].from_value(0.0)
		self.strafe_turn_blend = name_type_map['Float'].from_value(0.2)
		self._padding = name_type_map['Uint'](self.context, 0, None)
		self.turn_blend_limit = name_type_map['Float'].from_value(1.0)
		self.turn_speed_multiplier = name_type_map['Float'].from_value(1.0)
		self.flex_speed_multiplier = name_type_map['Float'].from_value(1.0)
		self.blend_space = name_type_map['Locomotion2BlendSpace'](self.context, 0, None)
		self.data_streams_count = name_type_map['Uint64'](self.context, 0, None)
		self.animations = name_type_map['ArrayPointer'](self.context, self.animation_count, name_type_map['Locomotion2AnimationInfo'])
		self.output_prop_through_variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.speed_variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.orientation_variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.data_streams = name_type_map['ArrayPointer'](self.context, self.data_streams_count, name_type_map['DataStreamResourceDataList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'animation_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'animations', name_type_map['ArrayPointer'], (None, name_type_map['Locomotion2AnimationInfo']), (False, None), (None, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'stopping_distance', name_type_map['Float'], (0, None), (False, 0.0), (None, None)
		yield 'strafe_turn_blend', name_type_map['Float'], (0, None), (False, 0.2), (None, None)
		yield '_padding', name_type_map['Uint'], (0, None), (False, None), (lambda context: (not context.user_version.use_djb) and (context.version >= 19), None)
		yield 'turn_blend_limit', name_type_map['Float'], (0, None), (False, 1.0), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'turn_speed_multiplier', name_type_map['Float'], (0, None), (False, 1.0), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'flex_speed_multiplier', name_type_map['Float'], (0, None), (False, 1.0), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'blend_space', name_type_map['Locomotion2BlendSpace'], (0, None), (False, None), (None, None)
		yield 'output_prop_through_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'speed_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'orientation_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'data_streams_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data_streams', name_type_map['ArrayPointer'], (None, name_type_map['DataStreamResourceDataList']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'animation_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'animations', name_type_map['ArrayPointer'], (instance.animation_count, name_type_map['Locomotion2AnimationInfo']), (False, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None)
		yield 'stopping_distance', name_type_map['Float'], (0, None), (False, 0.0)
		yield 'strafe_turn_blend', name_type_map['Float'], (0, None), (False, 0.2)
		if (not instance.context.user_version.use_djb) and (instance.context.version >= 19):
			yield '_padding', name_type_map['Uint'], (0, None), (False, None)
		if not ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)):
			yield 'turn_blend_limit', name_type_map['Float'], (0, None), (False, 1.0)
			yield 'turn_speed_multiplier', name_type_map['Float'], (0, None), (False, 1.0)
			yield 'flex_speed_multiplier', name_type_map['Float'], (0, None), (False, 1.0)
		yield 'blend_space', name_type_map['Locomotion2BlendSpace'], (0, None), (False, None)
		yield 'output_prop_through_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if not ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)):
			yield 'speed_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'orientation_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'data_streams_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data_streams', name_type_map['ArrayPointer'], (instance.data_streams_count, name_type_map['DataStreamResourceDataList']), (False, None)
