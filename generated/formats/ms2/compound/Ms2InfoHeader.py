import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.Buffer0 import Buffer0
from generated.formats.ms2.compound.BufferInfo import BufferInfo
from generated.formats.ms2.compound.BufferInfoPC import BufferInfoPC
from generated.formats.ms2.compound.BufferInfoZT import BufferInfoZT
from generated.formats.ms2.compound.ModelInfo import ModelInfo
from generated.formats.ms2.compound.ModelReader import ModelReader
from generated.formats.ms2.compound.Ms2SizedStrData import Ms2SizedStrData


class Ms2InfoHeader:

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_names_size = 0
		self.bone_info_size = 0
		self.info = Ms2SizedStrData(self.context, None, None)
		self.mdl_2_names = Array(self.context)
		self.buffer_0 = Buffer0(self.context, self.info, None)
		self.buffer_info = BufferInfo(self.context, None, None)
		self.buffer_info = BufferInfoZT(self.context, self.info.vertex_buffer_count, None)
		self.buffer_info = BufferInfoPC(self.context, None, None)
		self.model_infos = Array(self.context)

		# new style
		self.models_reader = ModelReader(self.context, self.model_infos, None)
		self.set_defaults()

	def set_defaults(self):
		self.bone_names_size = 0
		self.bone_info_size = 0
		self.info = Ms2SizedStrData(self.context, None, None)
		self.mdl_2_names = Array(self.context)
		self.buffer_0 = Buffer0(self.context, self.info, None)
		if self.context.version >= 47 and self.info.vertex_buffer_count:
			self.buffer_info = BufferInfo(self.context, None, None)
		if self.context.version == 13:
			self.buffer_info = BufferInfoZT(self.context, self.info.vertex_buffer_count, None)
		if self.context.version == 32:
			self.buffer_info = BufferInfoPC(self.context, None, None)
		self.model_infos = Array(self.context)
		self.models_reader = ModelReader(self.context, self.model_infos, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.bone_names_size = stream.read_uint()
		self.bone_info_size = stream.read_uint()
		self.info = stream.read_type(Ms2SizedStrData, (self.context, None, None))
		self.mdl_2_names = stream.read_zstrings((self.info.mdl_2_count))
		self.buffer_0 = stream.read_type(Buffer0, (self.context, self.info, None))
		if self.context.version >= 47 and self.info.vertex_buffer_count:
			self.buffer_info = stream.read_type(BufferInfo, (self.context, None, None))
		if self.context.version == 13:
			self.buffer_info = stream.read_type(BufferInfoZT, (self.context, self.info.vertex_buffer_count, None))
		if self.context.version == 32:
			self.buffer_info = stream.read_type(BufferInfoPC, (self.context, None, None))
		self.model_infos.read(stream, ModelInfo, self.info.mdl_2_count, None)
		self.models_reader = stream.read_type(ModelReader, (self.context, self.model_infos, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.bone_names_size)
		stream.write_uint(self.bone_info_size)
		stream.write_type(self.info)
		stream.write_zstrings(self.mdl_2_names)
		stream.write_type(self.buffer_0)
		if self.context.version >= 47 and self.info.vertex_buffer_count:
			stream.write_type(self.buffer_info)
		if self.context.version == 13:
			stream.write_type(self.buffer_info)
		if self.context.version == 32:
			stream.write_type(self.buffer_info)
		self.model_infos.write(stream, ModelInfo, self.info.mdl_2_count, None)
		stream.write_type(self.models_reader)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* bone_names_size = {self.bone_names_size.__repr__()}'
		s += f'\n	* bone_info_size = {self.bone_info_size.__repr__()}'
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* mdl_2_names = {self.mdl_2_names.__repr__()}'
		s += f'\n	* buffer_0 = {self.buffer_0.__repr__()}'
		s += f'\n	* buffer_info = {self.buffer_info.__repr__()}'
		s += f'\n	* model_infos = {self.model_infos.__repr__()}'
		s += f'\n	* models_reader = {self.models_reader.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
