from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.fgm.compound.AttributeInfo import AttributeInfo
from generated.formats.fgm.compound.FgmHeader import FgmHeader
from generated.formats.fgm.compound.TextureInfo import TextureInfo
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class FgmInfoHeader(GenericHeader):

	"""
	Custom header struct
	This reads a whole custom FGM file
	"""

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.data_lib_size = 0
		self.dependency_count = 0
		self.fgm_info = FgmHeader(self.context, None, None)
		self.texture_files = Array((self.dependency_count), ZString, self.context, None, None)
		self.textures = Array((self.fgm_info.texture_count), TextureInfo, self.context, None, None)
		self.attributes = Array((self.fgm_info.attribute_count), AttributeInfo, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.data_lib_size = 0
		self.dependency_count = 0
		self.fgm_info = FgmHeader(self.context, None, None)
		self.texture_files = Array((self.dependency_count), ZString, self.context, None, None)
		self.textures = Array((self.fgm_info.texture_count), TextureInfo, self.context, None, None)
		self.attributes = Array((self.fgm_info.attribute_count), AttributeInfo, self.context, None, None)

	def read(self, stream):
		super().read(stream)
		self.data_lib_size = stream.read_uint()
		self.dependency_count = stream.read_uint()
		self.fgm_info = stream.read_type(FgmHeader, (self.context, None, None))
		self.texture_files = stream.read_zstrings((self.dependency_count))
		self.textures.read(stream, TextureInfo, self.fgm_info.texture_count, None)
		self.attributes.read(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		super().write(stream)
		stream.write_uint(self.data_lib_size)
		stream.write_uint(self.dependency_count)
		stream.write_type(self.fgm_info)
		stream.write_zstrings(self.texture_files)
		self.textures.write(stream, TextureInfo, self.fgm_info.texture_count, None)
		self.attributes.write(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'FgmInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* data_lib_size = {self.data_lib_size.__repr__()}'
		s += f'\n	* dependency_count = {self.dependency_count.__repr__()}'
		s += f'\n	* fgm_info = {self.fgm_info.__repr__()}'
		s += f'\n	* texture_files = {self.texture_files.__repr__()}'
		s += f'\n	* textures = {self.textures.__repr__()}'
		s += f'\n	* attributes = {self.attributes.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
