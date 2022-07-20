from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class AkTrackSrcInfo:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.track_i_d = 0
		self.source_i_d = 0
		self.event_i_d = 0
		self.f_play_at = 0
		self.f_begin_trim_offset = 0
		self.f_end_trim_offset = 0
		self.f_src_duration = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.track_i_d = 0
		self.source_i_d = 0
		self.event_i_d = 0
		self.f_play_at = 0.0
		self.f_begin_trim_offset = 0.0
		self.f_end_trim_offset = 0.0
		self.f_src_duration = 0.0

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
		instance.track_i_d = stream.read_uint()
		instance.source_i_d = stream.read_uint()
		instance.event_i_d = stream.read_uint()
		instance.f_play_at = stream.read_double()
		instance.f_begin_trim_offset = stream.read_double()
		instance.f_end_trim_offset = stream.read_double()
		instance.f_src_duration = stream.read_double()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.track_i_d)
		stream.write_uint(instance.source_i_d)
		stream.write_uint(instance.event_i_d)
		stream.write_double(instance.f_play_at)
		stream.write_double(instance.f_begin_trim_offset)
		stream.write_double(instance.f_end_trim_offset)
		stream.write_double(instance.f_src_duration)

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
		return f'AkTrackSrcInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* track_i_d = {fmt_member(self.track_i_d, indent+1)}'
		s += f'\n	* source_i_d = {fmt_member(self.source_i_d, indent+1)}'
		s += f'\n	* event_i_d = {fmt_member(self.event_i_d, indent+1)}'
		s += f'\n	* f_play_at = {fmt_member(self.f_play_at, indent+1)}'
		s += f'\n	* f_begin_trim_offset = {fmt_member(self.f_begin_trim_offset, indent+1)}'
		s += f'\n	* f_end_trim_offset = {fmt_member(self.f_end_trim_offset, indent+1)}'
		s += f'\n	* f_src_duration = {fmt_member(self.f_src_duration, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
