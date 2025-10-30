from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkMusicTransSrcRule(BaseStruct):

	__name__ = 'AkMusicTransSrcRule'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.fade_params = name_type_map['FadeParams'](self.context, 0, None)
		self.e_sync_type = name_type_map['Uint'](self.context, 0, None)
		self.u_cue_filter_hash = name_type_map['Uint'](self.context, 0, None)
		self.b_play_post_exit = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'fade_params', name_type_map['FadeParams'], (0, None), (False, None), (None, None)
		yield 'e_sync_type', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'u_cue_filter_hash', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'b_play_post_exit', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fade_params', name_type_map['FadeParams'], (0, None), (False, None)
		yield 'e_sync_type', name_type_map['Uint'], (0, None), (False, None)
		yield 'u_cue_filter_hash', name_type_map['Uint'], (0, None), (False, None)
		yield 'b_play_post_exit', name_type_map['Ubyte'], (0, None), (False, None)
