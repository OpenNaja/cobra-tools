from generated.base_struct import BaseStruct
from generated.formats.base.basic import Double
from generated.formats.base.basic import Uint


class AkTrackSrcInfo(BaseStruct):

	__name__ = 'AkTrackSrcInfo'

	_import_key = 'bnk.compounds.AkTrackSrcInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.track_i_d = 0
		self.source_i_d = 0
		self.event_i_d = 0
		self.f_play_at = 0.0
		self.f_begin_trim_offset = 0.0
		self.f_end_trim_offset = 0.0
		self.f_src_duration = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('track_i_d', Uint, (0, None), (False, None), (None, None))
		yield ('source_i_d', Uint, (0, None), (False, None), (None, None))
		yield ('event_i_d', Uint, (0, None), (False, None), (None, None))
		yield ('f_play_at', Double, (0, None), (False, None), (None, None))
		yield ('f_begin_trim_offset', Double, (0, None), (False, None), (None, None))
		yield ('f_end_trim_offset', Double, (0, None), (False, None), (None, None))
		yield ('f_src_duration', Double, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'track_i_d', Uint, (0, None), (False, None)
		yield 'source_i_d', Uint, (0, None), (False, None)
		yield 'event_i_d', Uint, (0, None), (False, None)
		yield 'f_play_at', Double, (0, None), (False, None)
		yield 'f_begin_trim_offset', Double, (0, None), (False, None)
		yield 'f_end_trim_offset', Double, (0, None), (False, None)
		yield 'f_src_duration', Double, (0, None), (False, None)
