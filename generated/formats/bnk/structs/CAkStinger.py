from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class CAkStinger(BaseStruct):

	__name__ = 'CAkStinger'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.trigger_i_d = name_type_map['Uint'](self.context, 0, None)
		self.segment_i_d = name_type_map['Uint'](self.context, 0, None)
		self.sync_play_at = name_type_map['Uint'](self.context, 0, None)
		self.u_cue_filter_hash = name_type_map['Uint'](self.context, 0, None)
		self.dont_repeat_time = name_type_map['Int'](self.context, 0, None)
		self.num_segment_look_ahead = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'trigger_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'segment_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'sync_play_at', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'u_cue_filter_hash', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'dont_repeat_time', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'num_segment_look_ahead', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'trigger_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'segment_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'sync_play_at', name_type_map['Uint'], (0, None), (False, None)
		yield 'u_cue_filter_hash', name_type_map['Uint'], (0, None), (False, None)
		yield 'dont_repeat_time', name_type_map['Int'], (0, None), (False, None)
		yield 'num_segment_look_ahead', name_type_map['Uint'], (0, None), (False, None)
