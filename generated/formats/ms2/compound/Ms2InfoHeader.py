from generated.formats.ms2.compound.Ms2Buffer0 import Ms2Buffer0
from generated.formats.ms2.compound.Ms2BufferInfo import Ms2BufferInfo
from generated.formats.ms2.compound.Ms2SizedStrData import Ms2SizedStrData
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class Ms2InfoHeader(GenericHeader):

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_names_size = 0
		self.bone_info_size = 0
		self.general_info = Ms2SizedStrData(self.context, None, None)
		self.buffer_info = Ms2BufferInfo(self.context, None, None)
		self.buffer_0 = Ms2Buffer0(self.context, self.general_info, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.bone_names_size = 0
		self.bone_info_size = 0
		self.general_info = Ms2SizedStrData(self.context, None, None)
		if not (self.context.version < 19) and self.general_info.vertex_buffer_count:
			self.buffer_info = Ms2BufferInfo(self.context, None, None)
		self.buffer_0 = Ms2Buffer0(self.context, self.general_info, None)

	def read(self, stream):
		super().read(stream)
		self.bone_names_size = stream.read_uint()
		self.bone_info_size = stream.read_uint()
		self.general_info = stream.read_type(Ms2SizedStrData, (self.context, None, None))
		if not (self.context.version < 19) and self.general_info.vertex_buffer_count:
			self.buffer_info = stream.read_type(Ms2BufferInfo, (self.context, None, None))
		self.buffer_0 = stream.read_type(Ms2Buffer0, (self.context, self.general_info, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		super().write(stream)
		stream.write_uint(self.bone_names_size)
		stream.write_uint(self.bone_info_size)
		stream.write_type(self.general_info)
		if not (self.context.version < 19) and self.general_info.vertex_buffer_count:
			stream.write_type(self.buffer_info)
		stream.write_type(self.buffer_0)

		self.io_size = stream.tell() - self.io_start

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
