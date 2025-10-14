from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class PositioningData(BaseStruct):

	__name__ = 'PositioningData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_bits_3_d = name_type_map['Ubyte'](self.context, 0, None)
		self.e_path_mode = name_type_map['Ubyte'](self.context, 0, None)
		self.transition_time = name_type_map['Int'](self.context, 0, None)
		self.ul_num_vertices = name_type_map['Uint'](self.context, 0, None)
		self.vertices = Array(self.context, 0, None, (0,), name_type_map['AkPathVertex'])
		self.ul_num_play_list_item = name_type_map['Uint'](self.context, 0, None)
		self.p_play_list_items = Array(self.context, 0, None, (0,), name_type_map['AkPathListItemOffset'])
		self.ak_3_d_automation_params = Array(self.context, 0, None, (0,), name_type_map['Vec'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'u_bits_3_d', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'e_path_mode', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'transition_time', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'ul_num_vertices', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'vertices', Array, (0, None, (None,), name_type_map['AkPathVertex']), (False, None), (None, None)
		yield 'ul_num_play_list_item', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'p_play_list_items', Array, (0, None, (None,), name_type_map['AkPathListItemOffset']), (False, None), (None, None)
		yield 'ak_3_d_automation_params', Array, (0, None, (None,), name_type_map['Vec']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_bits_3_d', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'e_path_mode', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'transition_time', name_type_map['Int'], (0, None), (False, None)
		yield 'ul_num_vertices', name_type_map['Uint'], (0, None), (False, None)
		yield 'vertices', Array, (0, None, (instance.ul_num_vertices,), name_type_map['AkPathVertex']), (False, None)
		yield 'ul_num_play_list_item', name_type_map['Uint'], (0, None), (False, None)
		yield 'p_play_list_items', Array, (0, None, (instance.ul_num_play_list_item,), name_type_map['AkPathListItemOffset']), (False, None)
		yield 'ak_3_d_automation_params', Array, (0, None, (instance.ul_num_play_list_item,), name_type_map['Vec']), (False, None)
