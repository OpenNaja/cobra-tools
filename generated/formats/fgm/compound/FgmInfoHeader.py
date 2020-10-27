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
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FGM '
		self.magic = Array()
		self.version = 0
		self.flag_2 = 0

		# fragment count
		self.num_frags = 0

		# byte count to check for quirks
		self.tex_info_size = 0

		# byte count to check for quirks
		self.attr_info_size = 0

		# byte count to check for quirks
		self.zeros_size = 0

		# byte count to check for quirks
		self.data_lib_size = 0
		self.fgm_info = FourFragFgm()
		self.two_frags_pad = Array()
		self.textures = Array()
		self.texpad = Array()
		self.attributes = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic.read(stream, 'Byte', 4, None)
		self.version = stream.read_uint()
		stream.version = self.version
		self.flag_2 = stream.read_uint()
		self.num_frags = stream.read_uint()
		self.tex_info_size = stream.read_uint()
		self.attr_info_size = stream.read_uint()
		self.zeros_size = stream.read_uint()
		self.data_lib_size = stream.read_uint()
		self.fgm_info = stream.read_type(FourFragFgm)
		self.two_frags_pad.read(stream, TwoFragFgmExtra, self.num_frags == 2, None)
		self.textures.read(stream, TextureInfo, self.fgm_info.texture_count, None)
		self.texpad.read(stream, 'Byte', self.tex_info_size - (self.fgm_info.texture_count * 24), None)
		self.attributes.read(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.magic.write(stream, 'Byte', 4, None)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.flag_2)
		stream.write_uint(self.num_frags)
		stream.write_uint(self.tex_info_size)
		stream.write_uint(self.attr_info_size)
		stream.write_uint(self.zeros_size)
		stream.write_uint(self.data_lib_size)
		stream.write_type(self.fgm_info)
		self.two_frags_pad.write(stream, TwoFragFgmExtra, self.num_frags == 2, None)
		self.textures.write(stream, TextureInfo, self.fgm_info.texture_count, None)
		self.texpad.write(stream, 'Byte', self.tex_info_size - (self.fgm_info.texture_count * 24), None)
		self.attributes.write(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'FgmInfoHeader [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* magic = ' + self.magic.__repr__()
		s += '\n	* version = ' + self.version.__repr__()
		s += '\n	* flag_2 = ' + self.flag_2.__repr__()
		s += '\n	* num_frags = ' + self.num_frags.__repr__()
		s += '\n	* tex_info_size = ' + self.tex_info_size.__repr__()
		s += '\n	* attr_info_size = ' + self.attr_info_size.__repr__()
		s += '\n	* zeros_size = ' + self.zeros_size.__repr__()
		s += '\n	* data_lib_size = ' + self.data_lib_size.__repr__()
		s += '\n	* fgm_info = ' + self.fgm_info.__repr__()
		s += '\n	* two_frags_pad = ' + self.two_frags_pad.__repr__()
		s += '\n	* textures = ' + self.textures.__repr__()
		s += '\n	* texpad = ' + self.texpad.__repr__()
		s += '\n	* attributes = ' + self.attributes.__repr__()
		s += '\n'
		return s
