from generated.array import Array
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.imports import name_type_map


class MusicSwitch(HircObject):

	__name__ = 'MusicSwitch'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.music_node_params = name_type_map['MusicNodeParams'](self.context, 0, None)
		self.num_rules = name_type_map['Uint'](self.context, 0, None)
		self.rules = Array(self.context, 0, None, (0,), name_type_map['AkMusicTransitionRule'])
		self.b_is_continue_playback = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'music_node_params', name_type_map['MusicNodeParams'], (0, None), (False, None), (None, None)
		yield 'num_rules', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'rules', Array, (0, None, (None,), name_type_map['AkMusicTransitionRule']), (False, None), (None, None)
		yield 'b_is_continue_playback', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'music_node_params', name_type_map['MusicNodeParams'], (0, None), (False, None)
		yield 'num_rules', name_type_map['Uint'], (0, None), (False, None)
		yield 'rules', Array, (0, None, (instance.num_rules,), name_type_map['AkMusicTransitionRule']), (False, None)
		yield 'b_is_continue_playback', name_type_map['Ubyte'], (0, None), (False, None)
