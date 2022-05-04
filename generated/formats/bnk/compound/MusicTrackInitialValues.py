from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.bnk.compound.AkBankSourceData import AkBankSourceData
from generated.formats.bnk.compound.AkTrackSrcInfo import AkTrackSrcInfo
from generated.formats.bnk.compound.NodeBaseParams import NodeBaseParams


class MusicTrackInitialValues:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.u_flags = 0
		self.num_sources = 0
		self.p_source = Array((self.num_sources,), AkBankSourceData, self.context, 0, None)
		self.num_playlist_item = 0
		self.p_playlist = Array((self.num_playlist_item,), AkTrackSrcInfo, self.context, 0, None)
		self.num_sub_track = 0
		self.num_clip_automation_item = 0
		self.p_items = numpy.zeros((self.num_clip_automation_item,), dtype=numpy.dtype('uint32'))
		self.node_base_params = NodeBaseParams(self.context, 0, None)
		self.e_track_type = 0
		self.i_look_ahead_time = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.u_flags = 0
		self.num_sources = 0
		self.p_source = Array((self.num_sources,), AkBankSourceData, self.context, 0, None)
		self.num_playlist_item = 0
		self.p_playlist = Array((self.num_playlist_item,), AkTrackSrcInfo, self.context, 0, None)
		self.num_sub_track = 0
		self.num_clip_automation_item = 0
		self.p_items = numpy.zeros((self.num_clip_automation_item,), dtype=numpy.dtype('uint32'))
		self.node_base_params = NodeBaseParams(self.context, 0, None)
		self.e_track_type = 0
		self.i_look_ahead_time = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.u_flags = stream.read_ubyte()
		instance.num_sources = stream.read_uint()
		instance.p_source = Array.from_stream(stream, (instance.num_sources,), AkBankSourceData, instance.context, 0, None)
		instance.num_playlist_item = stream.read_uint()
		instance.p_playlist = Array.from_stream(stream, (instance.num_playlist_item,), AkTrackSrcInfo, instance.context, 0, None)
		instance.num_sub_track = stream.read_uint()
		instance.num_clip_automation_item = stream.read_uint()
		instance.p_items = stream.read_uints((instance.num_clip_automation_item,))
		instance.node_base_params = NodeBaseParams.from_stream(stream, instance.context, 0, None)
		instance.e_track_type = stream.read_ubyte()
		instance.i_look_ahead_time = stream.read_int()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ubyte(instance.u_flags)
		stream.write_uint(instance.num_sources)
		Array.to_stream(stream, instance.p_source, (instance.num_sources,), AkBankSourceData, instance.context, 0, None)
		stream.write_uint(instance.num_playlist_item)
		Array.to_stream(stream, instance.p_playlist, (instance.num_playlist_item,), AkTrackSrcInfo, instance.context, 0, None)
		stream.write_uint(instance.num_sub_track)
		stream.write_uint(instance.num_clip_automation_item)
		stream.write_uints(instance.p_items)
		NodeBaseParams.to_stream(stream, instance.node_base_params)
		stream.write_ubyte(instance.e_track_type)
		stream.write_int(instance.i_look_ahead_time)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'MusicTrackInitialValues [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* u_flags = {fmt_member(self.u_flags, indent+1)}'
		s += f'\n	* num_sources = {fmt_member(self.num_sources, indent+1)}'
		s += f'\n	* p_source = {fmt_member(self.p_source, indent+1)}'
		s += f'\n	* num_playlist_item = {fmt_member(self.num_playlist_item, indent+1)}'
		s += f'\n	* p_playlist = {fmt_member(self.p_playlist, indent+1)}'
		s += f'\n	* num_sub_track = {fmt_member(self.num_sub_track, indent+1)}'
		s += f'\n	* num_clip_automation_item = {fmt_member(self.num_clip_automation_item, indent+1)}'
		s += f'\n	* p_items = {fmt_member(self.p_items, indent+1)}'
		s += f'\n	* node_base_params = {fmt_member(self.node_base_params, indent+1)}'
		s += f'\n	* e_track_type = {fmt_member(self.e_track_type, indent+1)}'
		s += f'\n	* i_look_ahead_time = {fmt_member(self.i_look_ahead_time, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
