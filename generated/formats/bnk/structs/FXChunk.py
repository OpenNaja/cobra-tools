from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class FXChunk(BaseStruct):

	__name__ = 'FXChunk'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_f_x_index = name_type_map['Byte'](self.context, 0, None)
		self.fx_i_d = name_type_map['Uint'](self.context, 0, None)
		self.b_is_share_set = name_type_map['Byte'](self.context, 0, None)
		self.b_is_rendered = name_type_map['Byte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'u_f_x_index', name_type_map['Byte'], (0, None), (False, None), (None, None)
		yield 'fx_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'b_is_share_set', name_type_map['Byte'], (0, None), (False, None), (None, None)
		yield 'b_is_rendered', name_type_map['Byte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_f_x_index', name_type_map['Byte'], (0, None), (False, None)
		yield 'fx_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'b_is_share_set', name_type_map['Byte'], (0, None), (False, None)
		yield 'b_is_rendered', name_type_map['Byte'], (0, None), (False, None)
