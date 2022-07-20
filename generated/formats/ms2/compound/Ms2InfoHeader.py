from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString
from generated.formats.ms2.compound.Buffer0 import Buffer0
from generated.formats.ms2.compound.BufferInfo import BufferInfo
from generated.formats.ms2.compound.BufferPresence import BufferPresence
from generated.formats.ms2.compound.ModelInfo import ModelInfo
from generated.formats.ms2.compound.ModelReader import ModelReader
from generated.formats.ms2.compound.Ms2Root import Ms2Root


class Ms2InfoHeader:

	"""
	Custom header struct
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.biosyn = 0
		self.bone_info_size = 0
		self.info = 0

		# used since DLA
		self.buffers_presence = 0
		self.mdl_2_names = 0
		self.modelstream_names = 0
		self.modelstream_names = 0
		self.modelstream_names = 0
		self.buffer_0 = 0
		self.buffer_infos = 0
		self.model_infos = 0

		# handles interleaved (old) or separate (new) styles for models and bone infos
		self.models_reader = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.biosyn = 0
		self.bone_info_size = 0
		self.info = Ms2Root(self.context, 0, None)
		if self.context.version >= 7:
			self.buffers_presence = Array((self.info.vertex_buffer_count,), BufferPresence, self.context, 0, None)
		self.mdl_2_names = Array((self.info.mdl_2_count,), ZString, self.context, 0, None)
		if self.context.version <= 7 and self.info.vertex_buffer_count:
			self.modelstream_names = Array((self.info.vertex_buffer_count - self.info.stream_count,), ZString, self.context, 0, None)
		if 13 <= self.context.version <= 13 and self.info.vertex_buffer_count:
			self.modelstream_names = Array((self.info.vertex_buffer_count,), ZString, self.context, 0, None)
		if self.context.version >= 39 and self.info.vertex_buffer_count:
			self.modelstream_names = Array((self.info.stream_count,), ZString, self.context, 0, None)
		self.buffer_0 = Buffer0(self.context, self.info, None)
		self.buffer_infos = Array((self.info.vertex_buffer_count,), BufferInfo, self.context, 0, None)
		self.model_infos = Array((self.info.mdl_2_count,), ModelInfo, self.context, 0, None)
		self.models_reader = ModelReader(self.context, self.model_infos, None)

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
		instance.biosyn = stream.read_uint()
		instance.context.biosyn = instance.biosyn
		instance.bone_info_size = stream.read_uint()
		instance.info = Ms2Root.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 7:
			instance.buffers_presence = Array.from_stream(stream, (instance.info.vertex_buffer_count,), BufferPresence, instance.context, 0, None)
		instance.mdl_2_names = stream.read_zstrings((instance.info.mdl_2_count,))
		if instance.context.version <= 7 and instance.info.vertex_buffer_count:
			instance.modelstream_names = stream.read_zstrings((instance.info.vertex_buffer_count - instance.info.stream_count,))
		if 13 <= instance.context.version <= 13 and instance.info.vertex_buffer_count:
			instance.modelstream_names = stream.read_zstrings((instance.info.vertex_buffer_count,))
		if instance.context.version >= 39 and instance.info.vertex_buffer_count:
			instance.modelstream_names = stream.read_zstrings((instance.info.stream_count,))
		instance.buffer_0 = Buffer0.from_stream(stream, instance.context, instance.info, None)
		instance.buffer_infos = Array.from_stream(stream, (instance.info.vertex_buffer_count,), BufferInfo, instance.context, 0, None)
		instance.model_infos = Array.from_stream(stream, (instance.info.mdl_2_count,), ModelInfo, instance.context, 0, None)
		instance.models_reader = ModelReader.from_stream(stream, instance.context, instance.model_infos, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.biosyn)
		stream.write_uint(instance.bone_info_size)
		Ms2Root.to_stream(stream, instance.info)
		if instance.context.version >= 7:
			Array.to_stream(stream, instance.buffers_presence, (instance.info.vertex_buffer_count,), BufferPresence, instance.context, 0, None)
		stream.write_zstrings(instance.mdl_2_names)
		if instance.context.version <= 7 and instance.info.vertex_buffer_count:
			stream.write_zstrings(instance.modelstream_names)
		if 13 <= instance.context.version <= 13 and instance.info.vertex_buffer_count:
			stream.write_zstrings(instance.modelstream_names)
		if instance.context.version >= 39 and instance.info.vertex_buffer_count:
			stream.write_zstrings(instance.modelstream_names)
		Buffer0.to_stream(stream, instance.buffer_0)
		Array.to_stream(stream, instance.buffer_infos, (instance.info.vertex_buffer_count,), BufferInfo, instance.context, 0, None)
		Array.to_stream(stream, instance.model_infos, (instance.info.mdl_2_count,), ModelInfo, instance.context, 0, None)
		ModelReader.to_stream(stream, instance.models_reader)

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
		return f'Ms2InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* biosyn = {fmt_member(self.biosyn, indent+1)}'
		s += f'\n	* bone_info_size = {fmt_member(self.bone_info_size, indent+1)}'
		s += f'\n	* info = {fmt_member(self.info, indent+1)}'
		s += f'\n	* buffers_presence = {fmt_member(self.buffers_presence, indent+1)}'
		s += f'\n	* mdl_2_names = {fmt_member(self.mdl_2_names, indent+1)}'
		s += f'\n	* modelstream_names = {fmt_member(self.modelstream_names, indent+1)}'
		s += f'\n	* buffer_0 = {fmt_member(self.buffer_0, indent+1)}'
		s += f'\n	* buffer_infos = {fmt_member(self.buffer_infos, indent+1)}'
		s += f'\n	* model_infos = {fmt_member(self.model_infos, indent+1)}'
		s += f'\n	* models_reader = {fmt_member(self.models_reader, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
