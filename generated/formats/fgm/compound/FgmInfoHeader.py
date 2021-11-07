import numpy
import typing
from generated.array import Array
from generated.formats.fgm.compound.AttributeInfo import AttributeInfo
from generated.formats.fgm.compound.FourFragFgm import FourFragFgm
from generated.formats.fgm.compound.TextureInfo import TextureInfo
from generated.formats.fgm.compound.TwoFragFgmExtra import TwoFragFgmExtra
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class FgmInfoHeader(GenericHeader):

	"""
	Custom header struct
	
	This reads a whole custom FGM file
	"""

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

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
		self.texture_names = Array(self.context)
		self.fgm_info = FourFragFgm(self.context, None, None)
		self.two_frags_pad = Array(self.context)
		self.textures = Array(self.context)
		self.texpad = numpy.zeros((self.tex_info_size - (self.fgm_info.texture_count * 24)), dtype='byte')
		self.texpad = numpy.zeros((self.tex_info_size - (self.fgm_info.texture_count * 12)), dtype='byte')
		self.attributes = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.num_frags = 0
		self.num_textures = 0
		self.tex_info_size = 0
		self.attr_info_size = 0
		self.zeros_size = 0
		self.data_lib_size = 0
		self.texture_names = Array(self.context)
		self.fgm_info = FourFragFgm(self.context, None, None)
		self.two_frags_pad = Array(self.context)
		self.textures = Array(self.context)
		if not (self.context.version == 17):
			self.texpad = numpy.zeros((self.tex_info_size - (self.fgm_info.texture_count * 24)), dtype='byte')
		if self.context.version == 17:
			self.texpad = numpy.zeros((self.tex_info_size - (self.fgm_info.texture_count * 12)), dtype='byte')
		self.attributes = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.num_frags = stream.read_uint()
		self.num_textures = stream.read_uint()
		self.tex_info_size = stream.read_uint()
		self.attr_info_size = stream.read_uint()
		self.zeros_size = stream.read_uint()
		self.data_lib_size = stream.read_uint()
		self.texture_names = stream.read_zstrings((self.num_textures))
		self.fgm_info = stream.read_type(FourFragFgm, (self.context, None, None))
		self.two_frags_pad.read(stream, TwoFragFgmExtra, self.num_frags == 2, None)
		self.textures.read(stream, TextureInfo, self.fgm_info.texture_count, None)
		if not (self.context.version == 17):
			self.texpad = stream.read_bytes((self.tex_info_size - (self.fgm_info.texture_count * 24)))
		if self.context.version == 17:
			self.texpad = stream.read_bytes((self.tex_info_size - (self.fgm_info.texture_count * 12)))
		self.attributes.read(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
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
		if not (self.context.version == 17):
			stream.write_bytes(self.texpad)
		if self.context.version == 17:
			stream.write_bytes(self.texpad)
		self.attributes.write(stream, AttributeInfo, self.fgm_info.attribute_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'FgmInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
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
