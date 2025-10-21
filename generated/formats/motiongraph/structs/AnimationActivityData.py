from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AnimationActivityData(MemStruct):

	"""
	96 bytes
	"""

	__name__ = 'AnimationActivityData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.animation_flags = name_type_map['AnimationFlags'](self.context, 0, None)
		self.priorities = name_type_map['Uint'](self.context, 0, None)
		self.weight = name_type_map['FloatInputData'](self.context, 0, None)
		self.speed = name_type_map['FloatInputData'](self.context, 0, None)
		self.starting_prop_through = name_type_map['Float'](self.context, 0, None)
		self.lead_out_time = name_type_map['Float'](self.context, 0, None)
		self.count_6 = name_type_map['Uint64'](self.context, 0, None)
		self.additional_data_streams = name_type_map['DataStreamResourceDataList'](self.context, 0, None)
		self.mani = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.sync_prop_through_variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.output_prop_through_variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'mani', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'animation_flags', name_type_map['AnimationFlags'], (0, None), (False, None), (None, None)
		yield 'priorities', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'weight', name_type_map['FloatInputData'], (0, None), (False, None), (None, None)
		yield 'speed', name_type_map['FloatInputData'], (0, None), (False, None), (None, None)
		yield 'starting_prop_through', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'lead_out_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'sync_prop_through_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'count_6', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'output_prop_through_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'additional_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'mani', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'animation_flags', name_type_map['AnimationFlags'], (0, None), (False, None)
		yield 'priorities', name_type_map['Uint'], (0, None), (False, None)
		yield 'weight', name_type_map['FloatInputData'], (0, None), (False, None)
		yield 'speed', name_type_map['FloatInputData'], (0, None), (False, None)
		yield 'starting_prop_through', name_type_map['Float'], (0, None), (False, None)
		yield 'lead_out_time', name_type_map['Float'], (0, None), (False, None)
		yield 'sync_prop_through_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'count_6', name_type_map['Uint64'], (0, None), (False, None)
		yield 'output_prop_through_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'additional_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None)
