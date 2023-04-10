from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TurnActivityData(MemStruct):

	"""
	? bytes
	"""

	__name__ = 'TurnActivityData'

	_import_key = 'motiongraph.compounds.TurnActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.spot_data_streams = name_type_map['DataStreamResourceDataList'](self.context, 0, None)
		self.half_data_streams = name_type_map['DataStreamResourceDataList'](self.context, 0, None)
		self.full_data_streams = name_type_map['DataStreamResourceDataList'](self.context, 0, None)
		self.suppress_resource_data_streams = 0
		self._pad_0 = 0
		self.priorities = 0
		self.lead_out_time = 0.0
		self.flags = name_type_map['TurnFlags'](self.context, 0, None)
		self._pad_1 = 0
		self._pad_2 = 0
		self.max_angle = 0.0
		self.min_cycles = 0
		self.playback_rate = 0.0
		self.spot_animation = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.half_animation = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.full_animation = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.output_prop_through_variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('spot_animation', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('half_animation', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('full_animation', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('output_prop_through_variable', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('spot_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None), (None, None))
		yield ('half_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None), (None, None))
		yield ('full_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None), (None, None))
		yield ('suppress_resource_data_streams', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('_pad_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('priorities', name_type_map['Ushort'], (0, None), (False, None), (None, None))
		yield ('lead_out_time', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('flags', name_type_map['TurnFlags'], (0, None), (False, None), (None, None))
		yield ('_pad_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('_pad_2', name_type_map['Ushort'], (0, None), (False, None), (None, None))
		yield ('max_angle', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('min_cycles', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('playback_rate', name_type_map['Float'], (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'spot_animation', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'half_animation', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'full_animation', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'output_prop_through_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'spot_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None)
		yield 'half_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None)
		yield 'full_data_streams', name_type_map['DataStreamResourceDataList'], (0, None), (False, None)
		yield 'suppress_resource_data_streams', name_type_map['Ubyte'], (0, None), (False, None)
		yield '_pad_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'priorities', name_type_map['Ushort'], (0, None), (False, None)
		yield 'lead_out_time', name_type_map['Float'], (0, None), (False, None)
		yield 'flags', name_type_map['TurnFlags'], (0, None), (False, None)
		yield '_pad_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield '_pad_2', name_type_map['Ushort'], (0, None), (False, None)
		yield 'max_angle', name_type_map['Float'], (0, None), (False, None)
		yield 'min_cycles', name_type_map['Uint'], (0, None), (False, None)
		yield 'playback_rate', name_type_map['Float'], (0, None), (False, None)
