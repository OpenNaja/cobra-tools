import typing
from generated.array import Array
from generated.formats.fgm.compound.AttributeInfo import AttributeInfo
from generated.formats.fgm.compound.FourFragFgm import FourFragFgm
from generated.formats.fgm.compound.TextureInfo import TextureInfo
from generated.formats.fgm.compound.TwoFragFgmExtra import TwoFragFgmExtra


class FgmInfoHeader:

	"""
	Custom header struct
	
	This reads a whole custom FGM file
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FGM '
		self.magic = Array()

		# if 0x08 then 64bit, differentiates between ED and JWE, 0x08 for ED and PC
		self.version_flag = 0

		# 0x12 = PC, 0x13 = JWE, PZ
		self.version = 0

		# endianness?, usually zero
		self.bitswap = 0

		# always = 1
		self.seventh_byte = 1
		self.user_version = 0

		# fragment count
		self.num_frags = 0

		# texture ref count
		self.num_textures = 0

		# byte count to check for quirks
		self.tex_info_size = 0

		# byte count to check for quirks
		self.attr_info_size = 0

		# byte count to check for quirks
		self.zeros_size = 0

		# byte count to check for quirks
		self.data_lib_size = 0
		self.texture_names = Array()
		self.fgm_info = FourFragFgm()
		self.two_frags_pad = Array()
		self.textures = Array()
		self.texpad = Array()
		self.texpad = Array()
		self.attributes = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic = stream.read_bytes((4))
		self.version_flag = stream.read_byte()
		stream.version_flag = self.version_flag
		self.version = stream.read_byte()
		stream.version = self.version
		self.bitswap = stream.read_byte()
		self.seventh_byte = stream.read_byte()
		self.user_version = stream.read_uint()
		stream.user_version = self.user_version
		self.num_frags = stream.read_uint()
		self.num_textures = stream.read_uint()
		self.tex_info_size = stream.read_uint()
		self.attr_info_size = stream.read_uint()
		self.zeros_size = stream.read_uint()
		self.data_lib_size = stream.read_uint()
		self.texture_names = stream.read_zstrings((self.num_textures))
		self.fgm_info = stream.read_type(FourFragFgm)
		self.two_frags_pad.read(stream, TwoFragFgmExtra, self.num_frags == 2, None)
		self.textures.read(stream, TextureInfo, self.fgm_info.texture_count, None)
		if not (((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 8))):
			self.texpad = stream.read_bytes((self.tex_info_size - (self.fgm_info.texture_count * 24)))
		if ((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 8)):
			self.texpad = stream.read_bytes((self.tex_info_size - (self.fgm_info.texture_count * 12)))
		self.attributes.read(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_bytes(self.magic)
		stream.write_byte(self.version_flag)
		stream.version_flag = self.version_flag
		stream.write_byte(self.version)
		stream.version = self.version
		stream.write_byte(self.bitswap)
		stream.write_byte(self.seventh_byte)
		stream.write_uint(self.user_version)
		stream.user_version = self.user_version
		stream.write_uint(self.num_frags)
		stream.write_uint(self.num_textures)
		stream.write_uint(self.tex_info_size)
		stream.write_uint(self.attr_info_size)
		stream.write_uint(self.zeros_size)
		stream.write_uint(self.data_lib_size)
		stream.write_zstrings(self.texture_names)
		stream.write_type(self.fgm_info)
		self.two_frags_pad.write(stream, TwoFragFgmExtra, self.num_frags == 2, None)
		self.textures.write(stream, TextureInfo, self.fgm_info.texture_count, None)
		if not (((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 8))):
			stream.write_bytes(self.texpad)
		if ((stream.user_version == 24724) or (stream.user_version == 25108)) and ((stream.version == 19) and (stream.version_flag == 8)):
			stream.write_bytes(self.texpad)
		self.attributes.write(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'FgmInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* magic = {self.magic.__repr__()}'
		s += f'\n	* version_flag = {self.version_flag.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* bitswap = {self.bitswap.__repr__()}'
		s += f'\n	* seventh_byte = {self.seventh_byte.__repr__()}'
		s += f'\n	* user_version = {self.user_version.__repr__()}'
		s += f'\n	* num_frags = {self.num_frags.__repr__()}'
		s += f'\n	* num_textures = {self.num_textures.__repr__()}'
		s += f'\n	* tex_info_size = {self.tex_info_size.__repr__()}'
		s += f'\n	* attr_info_size = {self.attr_info_size.__repr__()}'
		s += f'\n	* zeros_size = {self.zeros_size.__repr__()}'
		s += f'\n	* data_lib_size = {self.data_lib_size.__repr__()}'
		s += f'\n	* texture_names = {self.texture_names.__repr__()}'
		s += f'\n	* fgm_info = {self.fgm_info.__repr__()}'
		s += f'\n	* two_frags_pad = {self.two_frags_pad.__repr__()}'
		s += f'\n	* textures = {self.textures.__repr__()}'
		s += f'\n	* texpad = {self.texpad.__repr__()}'
		s += f'\n	* attributes = {self.attributes.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
