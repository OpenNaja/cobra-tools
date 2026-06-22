from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class SwitchParams(BaseStruct):

	__name__ = 'SwitchParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.e_group_type = name_type_map['Ubyte'](self.context, 0, None)
		self.u_group_i_d = name_type_map['Uint'](self.context, 0, None)
		self.u_default_switch = name_type_map['Uint'](self.context, 0, None)
		self.num_switch_assoc = name_type_map['Uint'](self.context, 0, None)
		self.ul_switch_assoc = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'e_group_type', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'u_group_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'u_default_switch', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'num_switch_assoc', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ul_switch_assoc', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'e_group_type', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'u_group_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'u_default_switch', name_type_map['Uint'], (0, None), (False, None)
		yield 'num_switch_assoc', name_type_map['Uint'], (0, None), (False, None)
		yield 'ul_switch_assoc', Array, (0, None, (instance.num_switch_assoc,), name_type_map['Uint']), (False, None)
