from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class CAkLayer(BaseStruct):

	__name__ = 'CAkLayer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ul_layer_i_d = name_type_map['Uint'](self.context, 0, None)
		self.initial_r_t_p_c = name_type_map['InitialRTPC'](self.context, 0, None)
		self.rtpc_i_d = name_type_map['Uint'](self.context, 0, None)
		self.rtpc_type = name_type_map['Ubyte'](self.context, 0, None)
		self.ul_num_assoc = name_type_map['Uint'](self.context, 0, None)
		self.assocs = Array(self.context, 0, None, (0,), name_type_map['CAssociatedChildData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ul_layer_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'initial_r_t_p_c', name_type_map['InitialRTPC'], (0, None), (False, None), (None, None)
		yield 'rtpc_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'rtpc_type', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'ul_num_assoc', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'assocs', Array, (0, None, (None,), name_type_map['CAssociatedChildData']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ul_layer_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'initial_r_t_p_c', name_type_map['InitialRTPC'], (0, None), (False, None)
		yield 'rtpc_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'rtpc_type', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'ul_num_assoc', name_type_map['Uint'], (0, None), (False, None)
		yield 'assocs', Array, (0, None, (instance.ul_num_assoc,), name_type_map['CAssociatedChildData']), (False, None)
