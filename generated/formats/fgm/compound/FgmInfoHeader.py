from source.formats.base.basic import fmt_member
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

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.data_lib_size = 0
		self.dependency_count = 0
		self.fgm_info = FgmHeader(self.context, 0, None)
		self.texture_files = Array((self.dependency_count,), ZString, self.context, 0, None)
		self.textures = Array((self.fgm_info.texture_count,), TextureInfo, self.context, 0, None)
		self.attributes = Array((self.fgm_info.attribute_count,), AttributeInfo, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.data_lib_size = 0
		self.dependency_count = 0
		self.fgm_info = FgmHeader(self.context, 0, None)
		self.texture_files = Array((self.dependency_count,), ZString, self.context, 0, None)
		self.textures = Array((self.fgm_info.texture_count,), TextureInfo, self.context, 0, None)
		self.attributes = Array((self.fgm_info.attribute_count,), AttributeInfo, self.context, 0, None)

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
		instance.data_lib_size = stream.read_uint()
		instance.dependency_count = stream.read_uint()
		instance.fgm_info = FgmHeader.from_stream(stream, instance.context, 0, None)
		instance.texture_files = stream.read_zstrings((instance.dependency_count,))
		instance.textures = Array.from_stream(stream, (instance.fgm_info.texture_count,), TextureInfo, instance.context, 0, None)
		instance.attributes = Array.from_stream(stream, (instance.fgm_info.attribute_count,), AttributeInfo, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.data_lib_size)
		stream.write_uint(instance.dependency_count)
		FgmHeader.to_stream(stream, instance.fgm_info)
		stream.write_zstrings(instance.texture_files)
		Array.to_stream(stream, instance.textures, (instance.fgm_info.texture_count,), TextureInfo, instance.context, 0, None)
		Array.to_stream(stream, instance.attributes, (instance.fgm_info.attribute_count,), AttributeInfo, instance.context, 0, None)

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
		return f'FgmInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* data_lib_size = {fmt_member(self.data_lib_size, indent+1)}'
		s += f'\n	* dependency_count = {fmt_member(self.dependency_count, indent+1)}'
		s += f'\n	* fgm_info = {fmt_member(self.fgm_info, indent+1)}'
		s += f'\n	* texture_files = {fmt_member(self.texture_files, indent+1)}'
		s += f'\n	* textures = {fmt_member(self.textures, indent+1)}'
		s += f'\n	* attributes = {fmt_member(self.attributes, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
