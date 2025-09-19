from generated.array import Array
from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RandomSelectActivityActivityData(MemStruct):

	__name__ = 'RandomSelectActivityActivityData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = name_type_map['Uint'](self.context, 0, None)
		self.blend_in_time = name_type_map['Float'](self.context, 0, None)
		self.blend_out_time = name_type_map['Float'](self.context, 0, None)
		self.allow_restarting_activity = name_type_map['Ubyte'].from_value(0)
		self._pad_allow_restarting_activity = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.block_activity_restart_time = name_type_map['Float'].from_value(0.0)
		self.random_animation_flags = name_type_map['Uint'](self.context, 0, None)
		self.always_active = name_type_map['Ubyte'].from_value(0)
		self._pad_always_active = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.min_gap = name_type_map['Float'].from_value(7.0)
		self.max_gap = name_type_map['Float'].from_value(10.0)
		self._max_gap_pad = name_type_map['Uint'](self.context, 0, None)
		self.activities = name_type_map['ArrayPointer'](self.context, self.num_activities, name_type_map['RandomActivityActivityInfo'])
		self.random_number_var = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'activities', name_type_map['ArrayPointer'], (None, name_type_map['RandomActivityActivityInfo']), (False, None), (None, None)
		yield 'num_activities', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'blend_in_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'blend_out_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'allow_restarting_activity', name_type_map['Ubyte'], (0, None), (False, 0), (None, None)
		yield '_pad_allow_restarting_activity', Array, (0, None, (3,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'block_activity_restart_time', name_type_map['Float'], (0, None), (False, 0.0), (None, None)
		yield 'random_animation_flags', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'always_active', name_type_map['Ubyte'], (0, None), (False, 0), (None, None)
		yield '_pad_always_active', Array, (0, None, (3,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'min_gap', name_type_map['Float'], (0, None), (False, 7.0), (None, None)
		yield 'max_gap', name_type_map['Float'], (0, None), (False, 10.0), (None, None)
		yield '_max_gap_pad', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'random_number_var', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'activities', name_type_map['ArrayPointer'], (instance.num_activities, name_type_map['RandomActivityActivityInfo']), (False, None)
		yield 'num_activities', name_type_map['Uint'], (0, None), (False, None)
		yield 'blend_in_time', name_type_map['Float'], (0, None), (False, None)
		yield 'blend_out_time', name_type_map['Float'], (0, None), (False, None)
		yield 'allow_restarting_activity', name_type_map['Ubyte'], (0, None), (False, 0)
		yield '_pad_allow_restarting_activity', Array, (0, None, (3,), name_type_map['Ubyte']), (False, None)
		yield 'block_activity_restart_time', name_type_map['Float'], (0, None), (False, 0.0)
		yield 'random_animation_flags', name_type_map['Uint'], (0, None), (False, None)
		yield 'always_active', name_type_map['Ubyte'], (0, None), (False, 0)
		yield '_pad_always_active', Array, (0, None, (3,), name_type_map['Ubyte']), (False, None)
		yield 'min_gap', name_type_map['Float'], (0, None), (False, 7.0)
		yield 'max_gap', name_type_map['Float'], (0, None), (False, 10.0)
		yield '_max_gap_pad', name_type_map['Uint'], (0, None), (False, None)
		yield 'random_number_var', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
