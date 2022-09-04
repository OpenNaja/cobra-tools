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

	_import_path = 'generated.formats.bnk.compounds.MusicTrackInitialValues'

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

	def set_defaults(self):
		super().set_defaults()
		self.u_flags = 0
		self.num_sources = 0
		self.p_source = Array(self.context, 0, None, (self.num_sources,), AkBankSourceData)
		self.num_playlist_item = 0
		self.p_playlist = Array(self.context, 0, None, (self.num_playlist_item,), AkTrackSrcInfo)
		self.num_sub_track = 0
		self.num_clip_automation_item = 0
		self.p_items = numpy.zeros((self.num_clip_automation_item,), dtype=numpy.dtype('uint32'))
		self.node_base_params = NodeBaseParams(self.context, 0, None)
		self.e_track_type = 0
		self.i_look_ahead_time = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.u_flags = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.num_sources = Uint.from_stream(stream, instance.context, 0, None)
		instance.p_source = Array.from_stream(stream, instance.context, 0, None, (instance.num_sources,), AkBankSourceData)
		instance.num_playlist_item = Uint.from_stream(stream, instance.context, 0, None)
		instance.p_playlist = Array.from_stream(stream, instance.context, 0, None, (instance.num_playlist_item,), AkTrackSrcInfo)
		instance.num_sub_track = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_clip_automation_item = Uint.from_stream(stream, instance.context, 0, None)
		instance.p_items = Array.from_stream(stream, instance.context, 0, None, (instance.num_clip_automation_item,), Uint)
		instance.node_base_params = NodeBaseParams.from_stream(stream, instance.context, 0, None)
		instance.e_track_type = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.i_look_ahead_time = Int.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ubyte.to_stream(stream, instance.u_flags)
		Uint.to_stream(stream, instance.num_sources)
		Array.to_stream(stream, instance.p_source, instance.context, 0, None, (instance.num_sources,), AkBankSourceData)
		Uint.to_stream(stream, instance.num_playlist_item)
		Array.to_stream(stream, instance.p_playlist, instance.context, 0, None, (instance.num_playlist_item,), AkTrackSrcInfo)
		Uint.to_stream(stream, instance.num_sub_track)
		Uint.to_stream(stream, instance.num_clip_automation_item)
		Array.to_stream(stream, instance.p_items, instance.context, 0, None, (instance.num_clip_automation_item,), Uint)
		NodeBaseParams.to_stream(stream, instance.node_base_params)
		Ubyte.to_stream(stream, instance.e_track_type)
		Int.to_stream(stream, instance.i_look_ahead_time)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
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

	def get_info_str(self, indent=0):
		return f'MusicTrackInitialValues [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* u_flags = {self.fmt_member(self.u_flags, indent+1)}'
		s += f'\n	* num_sources = {self.fmt_member(self.num_sources, indent+1)}'
		s += f'\n	* p_source = {self.fmt_member(self.p_source, indent+1)}'
		s += f'\n	* num_playlist_item = {self.fmt_member(self.num_playlist_item, indent+1)}'
		s += f'\n	* p_playlist = {self.fmt_member(self.p_playlist, indent+1)}'
		s += f'\n	* num_sub_track = {self.fmt_member(self.num_sub_track, indent+1)}'
		s += f'\n	* num_clip_automation_item = {self.fmt_member(self.num_clip_automation_item, indent+1)}'
		s += f'\n	* p_items = {self.fmt_member(self.p_items, indent+1)}'
		s += f'\n	* node_base_params = {self.fmt_member(self.node_base_params, indent+1)}'
		s += f'\n	* e_track_type = {self.fmt_member(self.e_track_type, indent+1)}'
		s += f'\n	* i_look_ahead_time = {self.fmt_member(self.i_look_ahead_time, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
