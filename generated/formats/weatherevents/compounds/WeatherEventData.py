from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.weatherevents.imports import name_type_map


class WeatherEventData(MemStruct):

	__name__ = 'WeatherEventData'

	_import_key = 'weatherevents.compounds.WeatherEventData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.float_3 = 0.0
		self.float_4 = 0.0
		self.float_5 = 0.0
		self.float_6 = 0.0
		self.float_7 = 0.0
		self.float_8 = 0.0
		self.float_9 = 0.0
		self.float_10 = 0.0
		self.unk_1_as_1 = 0
		self.float_11 = 0.0
		self.float_12 = 0.0
		self.float_13 = 0.0
		self.float_14 = 0.0
		self.float_15 = 0.0
		self.block_1_unk_as_1 = 0
		self.block_1_float_1 = 0.0
		self.block_1_float_2 = 0.0
		self.block_1_float_3 = 0.0
		self.block_1_float_4 = 0.0
		self.block_1_float_5 = 0.0
		self.block_1_float_6 = 0.0
		self.block_1_float_7 = 0.0
		self.block_2_unk_as_1 = 0
		self.block_2_float_1 = 0.0
		self.block_2_float_2 = 0.0
		self.block_2_float_3 = 0.0
		self.block_2_float_4 = 0.0
		self.block_2_float_5 = 0.0
		self.block_2_float_6 = 0.0
		self.block_2_float_7 = 0.0
		self.block_3_unk_as_1 = 0
		self.block_3_float_1 = 0.0
		self.block_3_float_2 = 0.0
		self.block_3_float_3 = 0.0
		self.block_3_float_4 = 0.0
		self.block_3_float_5 = 0.0
		self.event_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.event_curve_name_from_base = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.event_curve_clouds = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('event_name', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('float_1', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_2', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_3', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_4', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_5', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_6', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_7', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_8', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_9', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_10', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('event_curve_name_from_base', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('unk_1_as_1', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('float_11', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_12', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_13', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_14', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('float_15', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('event_curve_clouds', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('block_1_unk_as_1', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('block_1_float_1', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_1_float_2', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_1_float_3', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_1_float_4', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_1_float_5', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_1_float_6', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_1_float_7', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_2_unk_as_1', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('block_2_float_1', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_2_float_2', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_2_float_3', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_2_float_4', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_2_float_5', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_2_float_6', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_2_float_7', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_3_unk_as_1', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('block_3_float_1', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_3_float_2', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_3_float_3', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_3_float_4', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('block_3_float_5', name_type_map['Float'], (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'event_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, None)
		yield 'float_4', name_type_map['Float'], (0, None), (False, None)
		yield 'float_5', name_type_map['Float'], (0, None), (False, None)
		yield 'float_6', name_type_map['Float'], (0, None), (False, None)
		yield 'float_7', name_type_map['Float'], (0, None), (False, None)
		yield 'float_8', name_type_map['Float'], (0, None), (False, None)
		yield 'float_9', name_type_map['Float'], (0, None), (False, None)
		yield 'float_10', name_type_map['Float'], (0, None), (False, None)
		yield 'event_curve_name_from_base', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_1_as_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'float_11', name_type_map['Float'], (0, None), (False, None)
		yield 'float_12', name_type_map['Float'], (0, None), (False, None)
		yield 'float_13', name_type_map['Float'], (0, None), (False, None)
		yield 'float_14', name_type_map['Float'], (0, None), (False, None)
		yield 'float_15', name_type_map['Float'], (0, None), (False, None)
		yield 'event_curve_clouds', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'block_1_unk_as_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'block_1_float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'block_1_float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'block_1_float_3', name_type_map['Float'], (0, None), (False, None)
		yield 'block_1_float_4', name_type_map['Float'], (0, None), (False, None)
		yield 'block_1_float_5', name_type_map['Float'], (0, None), (False, None)
		yield 'block_1_float_6', name_type_map['Float'], (0, None), (False, None)
		yield 'block_1_float_7', name_type_map['Float'], (0, None), (False, None)
		yield 'block_2_unk_as_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'block_2_float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'block_2_float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'block_2_float_3', name_type_map['Float'], (0, None), (False, None)
		yield 'block_2_float_4', name_type_map['Float'], (0, None), (False, None)
		yield 'block_2_float_5', name_type_map['Float'], (0, None), (False, None)
		yield 'block_2_float_6', name_type_map['Float'], (0, None), (False, None)
		yield 'block_2_float_7', name_type_map['Float'], (0, None), (False, None)
		yield 'block_3_unk_as_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'block_3_float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'block_3_float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'block_3_float_3', name_type_map['Float'], (0, None), (False, None)
		yield 'block_3_float_4', name_type_map['Float'], (0, None), (False, None)
		yield 'block_3_float_5', name_type_map['Float'], (0, None), (False, None)
