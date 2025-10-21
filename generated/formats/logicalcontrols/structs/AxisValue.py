from generated.formats.logicalcontrols.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AxisValue(MemStruct):

	__name__ = 'AxisValue'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk = name_type_map['Uint64'](self.context, 0, None)
		self.axis_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.button_1_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.button_2_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.combined_value_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.single_value_1_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.single_value_2_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'axis_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'button_1_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'button_2_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'combined_value_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'single_value_1_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'single_value_2_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'axis_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'button_1_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'button_2_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk', name_type_map['Uint64'], (0, None), (False, None)
		yield 'combined_value_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'single_value_1_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'single_value_2_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
