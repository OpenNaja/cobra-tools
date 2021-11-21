from generated.formats.ms2.compound.Ms2Buffer0 import Ms2Buffer0
from generated.formats.ms2.compound.Ms2BufferInfo import Ms2BufferInfo
from generated.formats.ms2.compound.Ms2SizedStrData import Ms2SizedStrData
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class Ms2InfoHeader(GenericHeader):

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_names_size = 0
		self.bone_info_size = 0
		self.general_info = Ms2SizedStrData(self.context, 0, None)
		self.buffer_info = Ms2BufferInfo(self.context, 0, None)
		self.buffer_0 = Ms2Buffer0(self.context, self.general_info, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.bone_names_size = 0
		self.bone_info_size = 0
		self.general_info = Ms2SizedStrData(self.context, 0, None)
		if not (self.context.version < 19) and self.general_info.vertex_buffer_count:
			self.buffer_info = Ms2BufferInfo(self.context, 0, None)
		self.buffer_0 = Ms2Buffer0(self.context, self.general_info, None)

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
		super().read_fields(stream, instance)
		instance.bone_names_size = stream.read_uint()
		instance.bone_info_size = stream.read_uint()
		instance.general_info = Ms2SizedStrData.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version < 19) and instance.general_info.vertex_buffer_count:
			instance.buffer_info = Ms2BufferInfo.from_stream(stream, instance.context, 0, None)
		instance.buffer_0 = Ms2Buffer0.from_stream(stream, instance.context, instance.general_info, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.bone_names_size)
		stream.write_uint(instance.bone_info_size)
		Ms2SizedStrData.to_stream(stream, instance.general_info)
		if not (instance.context.version < 19) and instance.general_info.vertex_buffer_count:
			Ms2BufferInfo.to_stream(stream, instance.buffer_info)
		Ms2Buffer0.to_stream(stream, instance.buffer_0)

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

	def get_info_str(self):
		return f'Ms2InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* bone_names_size = {self.bone_names_size.__repr__()}'
		s += f'\n	* bone_info_size = {self.bone_info_size.__repr__()}'
		s += f'\n	* general_info = {self.general_info.__repr__()}'
		s += f'\n	* buffer_info = {self.buffer_info.__repr__()}'
		s += f'\n	* buffer_0 = {self.buffer_0.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
