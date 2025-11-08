from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class CAssociatedChildData(BaseStruct):

	__name__ = 'CAssociatedChildData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ul_layer_i_d = name_type_map['Uint'](self.context, 0, None)
		self.ul_curve_size = name_type_map['Uint'](self.context, 0, None)
		self.p_r_t_p_c_mgr = Array(self.context, 0, None, (0,), name_type_map['AkRTPCGraphPoint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ul_layer_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ul_curve_size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'p_r_t_p_c_mgr', Array, (0, None, (None,), name_type_map['AkRTPCGraphPoint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ul_layer_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'ul_curve_size', name_type_map['Uint'], (0, None), (False, None)
		yield 'p_r_t_p_c_mgr', Array, (0, None, (instance.ul_curve_size,), name_type_map['AkRTPCGraphPoint']), (False, None)
