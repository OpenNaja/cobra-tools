import typing
from generated.formats.fgm.compound.AttributeInfo import AttributeInfo
from generated.formats.fgm.compound.FourFragFgm import FourFragFgm
from generated.formats.fgm.compound.TextureInfo import TextureInfo
from generated.formats.fgm.compound.TwoFragFgmExtra import TwoFragFgmExtra


class FgmInfoHeader:

	"""
	Custom header struct
	
	This reads a whole custom FGM file
	"""

	# 'FGM '
	magic: typing.List[int]
	version: int
	flag_2: int

	# fragment count
	num_frags: int

	# byte count to check for quirks
	tex_info_size: int

	# byte count to check for quirks
	attr_info_size: int

	# byte count to check for quirks
	zeros_size: int

	# byte count to check for quirks
	data_lib_size: int
	fgm_info: FourFragFgm
	two_frags_pad: typing.List[TwoFragFgmExtra]
	textures: typing.List[TextureInfo]
	texpad: typing.List[int]
	attributes: typing.List[AttributeInfo]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.magic = []
		self.version = 0
		self.flag_2 = 0
		self.num_frags = 0
		self.tex_info_size = 0
		self.attr_info_size = 0
		self.zeros_size = 0
		self.data_lib_size = 0
		self.fgm_info = FourFragFgm()
		self.two_frags_pad = []
		self.textures = []
		self.texpad = []
		self.attributes = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic = [stream.read_byte() for _ in range(4)]
		self.version = stream.read_uint()
		stream.version = self.version
		self.flag_2 = stream.read_uint()
		self.num_frags = stream.read_uint()
		self.tex_info_size = stream.read_uint()
		self.attr_info_size = stream.read_uint()
		self.zeros_size = stream.read_uint()
		self.data_lib_size = stream.read_uint()
		self.fgm_info = stream.read_type(FourFragFgm)
		self.two_frags_pad = [stream.read_type(TwoFragFgmExtra) for _ in range(self.num_frags == 2)]
		self.textures = [stream.read_type(TextureInfo) for _ in range(self.fgm_info.texture_count)]
		self.texpad = [stream.read_byte() for _ in range(self.tex_info_size - (self.fgm_info.texture_count * 24))]
		self.attributes = [stream.read_type(AttributeInfo) for _ in range(self.fgm_info.attribute_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		for item in self.magic: stream.write_byte(item)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.flag_2)
		stream.write_uint(self.num_frags)
		stream.write_uint(self.tex_info_size)
		stream.write_uint(self.attr_info_size)
		stream.write_uint(self.zeros_size)
		stream.write_uint(self.data_lib_size)
		stream.write_type(self.fgm_info)
		for item in self.two_frags_pad: stream.write_type(item)
		for item in self.textures: stream.write_type(item)
		for item in self.texpad: stream.write_byte(item)
		for item in self.attributes: stream.write_type(item)

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
