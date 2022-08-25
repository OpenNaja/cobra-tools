from generated.base_struct import BaseStruct
from generated.formats.base.basic import Double
from generated.formats.base.basic import Uint


class AkTrackSrcInfo(BaseStruct):

	__name__ = AkTrackSrcInfo

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

	def set_defaults(self):
		super().set_defaults()
		self.track_i_d = 0
		self.source_i_d = 0
		self.event_i_d = 0
		self.f_play_at = 0.0
		self.f_begin_trim_offset = 0.0
		self.f_end_trim_offset = 0.0
		self.f_src_duration = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.track_i_d = Uint.from_stream(stream, instance.context, 0, None)
		instance.source_i_d = Uint.from_stream(stream, instance.context, 0, None)
		instance.event_i_d = Uint.from_stream(stream, instance.context, 0, None)
		instance.f_play_at = Double.from_stream(stream, instance.context, 0, None)
		instance.f_begin_trim_offset = Double.from_stream(stream, instance.context, 0, None)
		instance.f_end_trim_offset = Double.from_stream(stream, instance.context, 0, None)
		instance.f_src_duration = Double.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.track_i_d)
		Uint.to_stream(stream, instance.source_i_d)
		Uint.to_stream(stream, instance.event_i_d)
		Double.to_stream(stream, instance.f_play_at)
		Double.to_stream(stream, instance.f_begin_trim_offset)
		Double.to_stream(stream, instance.f_end_trim_offset)
		Double.to_stream(stream, instance.f_src_duration)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'track_i_d', Uint, (0, None), (False, None)
		yield 'source_i_d', Uint, (0, None), (False, None)
		yield 'event_i_d', Uint, (0, None), (False, None)
		yield 'f_play_at', Double, (0, None), (False, None)
		yield 'f_begin_trim_offset', Double, (0, None), (False, None)
		yield 'f_end_trim_offset', Double, (0, None), (False, None)
		yield 'f_src_duration', Double, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AkTrackSrcInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* track_i_d = {self.fmt_member(self.track_i_d, indent+1)}'
		s += f'\n	* source_i_d = {self.fmt_member(self.source_i_d, indent+1)}'
		s += f'\n	* event_i_d = {self.fmt_member(self.event_i_d, indent+1)}'
		s += f'\n	* f_play_at = {self.fmt_member(self.f_play_at, indent+1)}'
		s += f'\n	* f_begin_trim_offset = {self.fmt_member(self.f_begin_trim_offset, indent+1)}'
		s += f'\n	* f_end_trim_offset = {self.fmt_member(self.f_end_trim_offset, indent+1)}'
		s += f'\n	* f_src_duration = {self.fmt_member(self.f_src_duration, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
