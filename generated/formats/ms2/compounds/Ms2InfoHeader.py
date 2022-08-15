from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ms2.compounds.Buffer0 import Buffer0
from generated.formats.ms2.compounds.BufferInfo import BufferInfo
from generated.formats.ms2.compounds.BufferPresence import BufferPresence
from generated.formats.ms2.compounds.ModelInfo import ModelInfo
from generated.formats.ms2.compounds.ModelReader import ModelReader
from generated.formats.ms2.compounds.Ms2Root import Ms2Root


class Ms2InfoHeader(BaseStruct):

	"""
	Custom header struct
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.biosyn = 0
		self.bone_info_size = 0
		self.info = Ms2Root(self.context, 0, None)

		# used since DLA
		self.buffers_presence = Array((self.info.vertex_buffer_count,), BufferPresence, self.context, 0, None)
		self.mdl_2_names = Array((self.info.mdl_2_count,), ZString, self.context, 0, None)
		self.modelstream_names = Array((self.info.stream_count,), ZString, self.context, 0, None)
		self.buffer_0 = Buffer0(self.context, self.info, None)
		self.buffer_infos = Array((self.info.vertex_buffer_count,), BufferInfo, self.context, 0, None)
		self.model_infos = Array((self.info.mdl_2_count,), ModelInfo, self.context, 0, None)

		# handles interleaved (old) or separate (new) styles for models and bone infos
		self.models_reader = ModelReader(self.context, self.model_infos, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.biosyn = Uint.from_stream(stream, instance.context, 0, None)
		instance.context.biosyn = instance.biosyn
		instance.bone_info_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.info = Ms2Root.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 7:
			instance.buffers_presence = Array.from_stream(stream, instance.context, 0, None, (instance.info.vertex_buffer_count,), BufferPresence)
		instance.mdl_2_names = Array.from_stream(stream, instance.context, 0, None, (instance.info.mdl_2_count,), ZString)
		if instance.context.version <= 7 and instance.info.vertex_buffer_count:
			instance.modelstream_names = Array.from_stream(stream, instance.context, 0, None, (instance.info.vertex_buffer_count - instance.info.stream_count,), ZString)
		if 13 <= instance.context.version <= 13 and instance.info.vertex_buffer_count:
			instance.modelstream_names = Array.from_stream(stream, instance.context, 0, None, (instance.info.vertex_buffer_count,), ZString)
		if instance.context.version >= 39 and instance.info.vertex_buffer_count:
			instance.modelstream_names = Array.from_stream(stream, instance.context, 0, None, (instance.info.stream_count,), ZString)
		instance.buffer_0 = Buffer0.from_stream(stream, instance.context, instance.info, None)
		instance.buffer_infos = Array.from_stream(stream, instance.context, 0, None, (instance.info.vertex_buffer_count,), BufferInfo)
		instance.model_infos = Array.from_stream(stream, instance.context, 0, None, (instance.info.mdl_2_count,), ModelInfo)
		instance.models_reader = ModelReader.from_stream(stream, instance.context, instance.model_infos, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.biosyn)
		Uint.to_stream(stream, instance.bone_info_size)
		Ms2Root.to_stream(stream, instance.info)
		if instance.context.version >= 7:
			Array.to_stream(stream, instance.buffers_presence, (instance.info.vertex_buffer_count,), BufferPresence, instance.context, 0, None)
		Array.to_stream(stream, instance.mdl_2_names, (instance.info.mdl_2_count,), ZString, instance.context, 0, None)
		if instance.context.version <= 7 and instance.info.vertex_buffer_count:
			Array.to_stream(stream, instance.modelstream_names, (instance.info.vertex_buffer_count - instance.info.stream_count,), ZString, instance.context, 0, None)
		if 13 <= instance.context.version <= 13 and instance.info.vertex_buffer_count:
			Array.to_stream(stream, instance.modelstream_names, (instance.info.vertex_buffer_count,), ZString, instance.context, 0, None)
		if instance.context.version >= 39 and instance.info.vertex_buffer_count:
			Array.to_stream(stream, instance.modelstream_names, (instance.info.stream_count,), ZString, instance.context, 0, None)
		Buffer0.to_stream(stream, instance.buffer_0)
		Array.to_stream(stream, instance.buffer_infos, (instance.info.vertex_buffer_count,), BufferInfo, instance.context, 0, None)
		Array.to_stream(stream, instance.model_infos, (instance.info.mdl_2_count,), ModelInfo, instance.context, 0, None)
		ModelReader.to_stream(stream, instance.models_reader)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'biosyn', Uint, (0, None)
		yield 'bone_info_size', Uint, (0, None)
		yield 'info', Ms2Root, (0, None)
		if instance.context.version >= 7:
			yield 'buffers_presence', Array, ((instance.info.vertex_buffer_count,), BufferPresence, 0, None)
		yield 'mdl_2_names', Array, ((instance.info.mdl_2_count,), ZString, 0, None)
		if instance.context.version <= 7 and instance.info.vertex_buffer_count:
			yield 'modelstream_names', Array, ((instance.info.vertex_buffer_count - instance.info.stream_count,), ZString, 0, None)
		if 13 <= instance.context.version <= 13 and instance.info.vertex_buffer_count:
			yield 'modelstream_names', Array, ((instance.info.vertex_buffer_count,), ZString, 0, None)
		if instance.context.version >= 39 and instance.info.vertex_buffer_count:
			yield 'modelstream_names', Array, ((instance.info.stream_count,), ZString, 0, None)
		yield 'buffer_0', Buffer0, (instance.info, None)
		yield 'buffer_infos', Array, ((instance.info.vertex_buffer_count,), BufferInfo, 0, None)
		yield 'model_infos', Array, ((instance.info.mdl_2_count,), ModelInfo, 0, None)
		yield 'models_reader', ModelReader, (instance.model_infos, None)

	def get_info_str(self, indent=0):
		return f'Ms2InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* biosyn = {self.fmt_member(self.biosyn, indent+1)}'
		s += f'\n	* bone_info_size = {self.fmt_member(self.bone_info_size, indent+1)}'
		s += f'\n	* info = {self.fmt_member(self.info, indent+1)}'
		s += f'\n	* buffers_presence = {self.fmt_member(self.buffers_presence, indent+1)}'
		s += f'\n	* mdl_2_names = {self.fmt_member(self.mdl_2_names, indent+1)}'
		s += f'\n	* modelstream_names = {self.fmt_member(self.modelstream_names, indent+1)}'
		s += f'\n	* buffer_0 = {self.fmt_member(self.buffer_0, indent+1)}'
		s += f'\n	* buffer_infos = {self.fmt_member(self.buffer_infos, indent+1)}'
		s += f'\n	* model_infos = {self.fmt_member(self.model_infos, indent+1)}'
		s += f'\n	* models_reader = {self.fmt_member(self.models_reader, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
