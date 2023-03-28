import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.bnk.compounds.AkBankSourceData import AkBankSourceData
from generated.formats.bnk.compounds.AkTrackSrcInfo import AkTrackSrcInfo
from generated.formats.bnk.compounds.NodeBaseParams import NodeBaseParams


class MusicTrackInitialValues(BaseStruct):

	__name__ = 'MusicTrackInitialValues'

	_import_key = 'bnk.compounds.MusicTrackInitialValues'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_flags = 0
		self.num_sources = 0
		self.p_source = Array(self.context, 0, None, (0,), AkBankSourceData)
		self.num_playlist_item = 0
		self.p_playlist = Array(self.context, 0, None, (0,), AkTrackSrcInfo)
		self.num_sub_track = 0
		self.num_clip_automation_item = 0
		self.p_items = Array(self.context, 0, None, (0,), Uint)
		self.node_base_params = NodeBaseParams(self.context, 0, None)
		self.e_track_type = 0
		self.i_look_ahead_time = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('u_flags', Ubyte, (0, None), (False, None), None)
		yield ('num_sources', Uint, (0, None), (False, None), None)
		yield ('p_source', Array, (0, None, (None,), AkBankSourceData), (False, None), None)
		yield ('num_playlist_item', Uint, (0, None), (False, None), None)
		yield ('p_playlist', Array, (0, None, (None,), AkTrackSrcInfo), (False, None), None)
		yield ('num_sub_track', Uint, (0, None), (False, None), None)
		yield ('num_clip_automation_item', Uint, (0, None), (False, None), None)
		yield ('p_items', Array, (0, None, (None,), Uint), (False, None), None)
		yield ('node_base_params', NodeBaseParams, (0, None), (False, None), None)
		yield ('e_track_type', Ubyte, (0, None), (False, None), None)
		yield ('i_look_ahead_time', Int, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_flags', Ubyte, (0, None), (False, None)
		yield 'num_sources', Uint, (0, None), (False, None)
		yield 'p_source', Array, (0, None, (instance.num_sources,), AkBankSourceData), (False, None)
		yield 'num_playlist_item', Uint, (0, None), (False, None)
		yield 'p_playlist', Array, (0, None, (instance.num_playlist_item,), AkTrackSrcInfo), (False, None)
		yield 'num_sub_track', Uint, (0, None), (False, None)
		yield 'num_clip_automation_item', Uint, (0, None), (False, None)
		yield 'p_items', Array, (0, None, (instance.num_clip_automation_item,), Uint), (False, None)
		yield 'node_base_params', NodeBaseParams, (0, None), (False, None)
		yield 'e_track_type', Ubyte, (0, None), (False, None)
		yield 'i_look_ahead_time', Int, (0, None), (False, None)


MusicTrackInitialValues.init_attributes()
