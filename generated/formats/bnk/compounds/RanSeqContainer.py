from generated.array import Array
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.imports import name_type_map


class RanSeqContainer(HircObject):

	"""
	wwiser CAkRanSeqCntr__SetInitialValues
	"""

	__name__ = 'RanSeqContainer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.s_loop_count = name_type_map['Ushort'](self.context, 0, None)
		self.s_loop_mod_min = name_type_map['Ushort'](self.context, 0, None)
		self.s_loop_mod_max = name_type_map['Ushort'](self.context, 0, None)
		self.f_transition_time = name_type_map['Float'](self.context, 0, None)
		self.f_transition_time_mod_min = name_type_map['Float'](self.context, 0, None)
		self.f_transition_time_mod_max = name_type_map['Float'](self.context, 0, None)
		self.w_avoid_repeat_count = name_type_map['Ushort'](self.context, 0, None)
		self.e_transition_mode = name_type_map['Ubyte'](self.context, 0, None)
		self.e_random_mode = name_type_map['Ubyte'](self.context, 0, None)
		self.e_mode = name_type_map['Ubyte'](self.context, 0, None)
		self.by_bit_vector = name_type_map['Ubyte'](self.context, 0, None)
		self.num_children = name_type_map['Uint'](self.context, 0, None)
		self.children = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.num_play_list_item = name_type_map['Ushort'](self.context, 0, None)
		self.play_list_item = Array(self.context, 0, None, (0,), name_type_map['AkPlaylistItem'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None), (None, None)
		yield 's_loop_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 's_loop_mod_min', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 's_loop_mod_max', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'f_transition_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'f_transition_time_mod_min', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'f_transition_time_mod_max', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'w_avoid_repeat_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'e_transition_mode', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'e_random_mode', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'e_mode', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_children', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'children', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'num_play_list_item', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'play_list_item', Array, (0, None, (None,), name_type_map['AkPlaylistItem']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None)
		yield 's_loop_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 's_loop_mod_min', name_type_map['Ushort'], (0, None), (False, None)
		yield 's_loop_mod_max', name_type_map['Ushort'], (0, None), (False, None)
		yield 'f_transition_time', name_type_map['Float'], (0, None), (False, None)
		yield 'f_transition_time_mod_min', name_type_map['Float'], (0, None), (False, None)
		yield 'f_transition_time_mod_max', name_type_map['Float'], (0, None), (False, None)
		yield 'w_avoid_repeat_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'e_transition_mode', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'e_random_mode', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'e_mode', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_children', name_type_map['Uint'], (0, None), (False, None)
		yield 'children', Array, (0, None, (instance.num_children,), name_type_map['Uint']), (False, None)
		yield 'num_play_list_item', name_type_map['Ushort'], (0, None), (False, None)
		yield 'play_list_item', Array, (0, None, (instance.num_play_list_item,), name_type_map['AkPlaylistItem']), (False, None)
