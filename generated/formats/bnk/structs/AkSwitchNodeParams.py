from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkSwitchNodeParams(BaseStruct):

	__name__ = 'AkSwitchNodeParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ul_node_i_d = name_type_map['Uint'](self.context, 0, None)
		self.by_bit_vector_1 = name_type_map['Ubyte'](self.context, 0, None)
		self.by_bit_vector_2 = name_type_map['Ubyte'](self.context, 0, None)
		self.fade_out_time = name_type_map['Int'](self.context, 0, None)
		self.fade_in_time = name_type_map['Int'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ul_node_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'by_bit_vector_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'by_bit_vector_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'fade_out_time', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'fade_in_time', name_type_map['Int'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ul_node_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'by_bit_vector_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'by_bit_vector_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'fade_out_time', name_type_map['Int'], (0, None), (False, None)
		yield 'fade_in_time', name_type_map['Int'], (0, None), (False, None)
