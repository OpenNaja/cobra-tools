import generated.formats.ms2.compounds.BufferInfo
import generated.formats.ms2.compounds.BufferPresence
import generated.formats.ms2.compounds.ModelInfo
import numpy
from generated.array import Array
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Ms2Root(MemStruct):

	"""
	root header of the ms2
	48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# see version tag
		self.version = 0

		# total count of vertex buffers, including streamed buffers
		self.vertex_buffer_count = 0
		self.mdl_2_count = 0

		# count of names in ms2 buffer0
		self.name_count = 0

		# -1 if there is no vertex buffer at all; else count of static buffers
		self.stream_count = 0
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

		# ms2's static buffer_info or empty (if no buffers)
		self.buffer_infos = ArrayPointer(self.context, self.vertex_buffer_count, generated.formats.ms2.compounds.BufferInfo.BufferInfo)

		# one for each mdl2
		self.model_infos = ArrayPointer(self.context, self.mdl_2_count, generated.formats.ms2.compounds.ModelInfo.ModelInfo)

		# data as in get_buffer_presence()
		self.buffers_presence = ArrayPointer(self.context, self.vertex_buffer_count, generated.formats.ms2.compounds.BufferPresence.BufferPresence)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.version = 0
		self.vertex_buffer_count = 0
		self.mdl_2_count = 0
		self.name_count = 0
		self.stream_count = 0
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))
		self.buffer_infos = ArrayPointer(self.context, self.vertex_buffer_count, generated.formats.ms2.compounds.BufferInfo.BufferInfo)
		self.model_infos = ArrayPointer(self.context, self.mdl_2_count, generated.formats.ms2.compounds.ModelInfo.ModelInfo)
		self.buffers_presence = ArrayPointer(self.context, self.vertex_buffer_count, generated.formats.ms2.compounds.BufferPresence.BufferPresence)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.version = stream.read_uint()
		instance.context.version = instance.version
		instance.vertex_buffer_count = stream.read_ushort()
		instance.mdl_2_count = stream.read_ushort()
		instance.name_count = stream.read_ushort()
		instance.stream_count = stream.read_short()
		instance.zeros = stream.read_uints((3,))
		instance.buffer_infos = ArrayPointer.from_stream(stream, instance.context, instance.vertex_buffer_count, generated.formats.ms2.compounds.BufferInfo.BufferInfo)
		instance.model_infos = ArrayPointer.from_stream(stream, instance.context, instance.mdl_2_count, generated.formats.ms2.compounds.ModelInfo.ModelInfo)
		instance.buffers_presence = ArrayPointer.from_stream(stream, instance.context, instance.vertex_buffer_count, generated.formats.ms2.compounds.BufferPresence.BufferPresence)
		if not isinstance(instance.buffer_infos, int):
			instance.buffer_infos.arg = instance.vertex_buffer_count
		if not isinstance(instance.model_infos, int):
			instance.model_infos.arg = instance.mdl_2_count
		if not isinstance(instance.buffers_presence, int):
			instance.buffers_presence.arg = instance.vertex_buffer_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.version)
		stream.write_ushort(instance.vertex_buffer_count)
		stream.write_ushort(instance.mdl_2_count)
		stream.write_ushort(instance.name_count)
		stream.write_short(instance.stream_count)
		stream.write_uints(instance.zeros)
		ArrayPointer.to_stream(stream, instance.buffer_infos)
		ArrayPointer.to_stream(stream, instance.model_infos)
		ArrayPointer.to_stream(stream, instance.buffers_presence)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'version', Uint, (0, None)
		yield 'vertex_buffer_count', Ushort, (0, None)
		yield 'mdl_2_count', Ushort, (0, None)
		yield 'name_count', Ushort, (0, None)
		yield 'stream_count', Short, (0, None)
		yield 'zeros', Array, ((3,), Uint, 0, None)
		yield 'buffer_infos', ArrayPointer, (instance.vertex_buffer_count, generated.formats.ms2.compounds.BufferInfo.BufferInfo)
		yield 'model_infos', ArrayPointer, (instance.mdl_2_count, generated.formats.ms2.compounds.ModelInfo.ModelInfo)
		yield 'buffers_presence', ArrayPointer, (instance.vertex_buffer_count, generated.formats.ms2.compounds.BufferPresence.BufferPresence)

	def get_info_str(self, indent=0):
		return f'Ms2Root [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* version = {self.fmt_member(self.version, indent+1)}'
		s += f'\n	* vertex_buffer_count = {self.fmt_member(self.vertex_buffer_count, indent+1)}'
		s += f'\n	* mdl_2_count = {self.fmt_member(self.mdl_2_count, indent+1)}'
		s += f'\n	* name_count = {self.fmt_member(self.name_count, indent+1)}'
		s += f'\n	* stream_count = {self.fmt_member(self.stream_count, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		s += f'\n	* buffer_infos = {self.fmt_member(self.buffer_infos, indent+1)}'
		s += f'\n	* model_infos = {self.fmt_member(self.model_infos, indent+1)}'
		s += f'\n	* buffers_presence = {self.fmt_member(self.buffers_presence, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
