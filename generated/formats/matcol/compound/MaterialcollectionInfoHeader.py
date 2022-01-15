import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.matcol.compound.LayeredWrapper import LayeredWrapper
from generated.formats.matcol.compound.MatcolRoot import MatcolRoot
from generated.formats.matcol.compound.RootFrag import RootFrag
from generated.formats.matcol.compound.Texture import Texture
from generated.formats.matcol.compound.TextureWrapper import TextureWrapper
from generated.formats.matcol.compound.VariantWrapper import VariantWrapper


class MaterialcollectionInfoHeader:

	"""
	Custom header struct
	
	This reads a whole custom Matcol file
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FGM '
		self.magic = numpy.zeros((4), dtype='byte')
		self.version = 0
		self.user_version = 0
		self.root = MatcolRoot(self.context, None, None)
		self.info = RootFrag(self.context, None, None)
		self.textures = Array(self.context)
		self.texture_wrapper = TextureWrapper(self.context, None, None)
		self.variant_wrapper = VariantWrapper(self.context, None, None)
		self.layered_wrapper = LayeredWrapper(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.magic = numpy.zeros((4), dtype='byte')
		self.version = 0
		self.user_version = 0
		self.root = MatcolRoot(self.context, None, None)
		self.info = RootFrag(self.context, None, None)
		self.textures = Array(self.context)
		self.texture_wrapper = TextureWrapper(self.context, None, None)
		if self.root_1.flag == 3:
			self.variant_wrapper = VariantWrapper(self.context, None, None)
		if self.root_1.flag == 2:
			self.layered_wrapper = LayeredWrapper(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.magic = stream.read_bytes((4))
		self.version = stream.read_uint()
		self.context.version = self.version
		self.user_version = stream.read_uint()
		self.context.user_version = self.user_version
		self.root = stream.read_type(MatcolRoot, (self.context, None, None))
		self.info = stream.read_type(RootFrag, (self.context, None, None))
		self.textures.read(stream, Texture, self.info.texture_count, None)
		self.texture_wrapper = stream.read_type(TextureWrapper, (self.context, None, None))
		if self.root_1.flag == 3:
			self.variant_wrapper = stream.read_type(VariantWrapper, (self.context, None, None))
		if self.root_1.flag == 2:
			self.layered_wrapper = stream.read_type(LayeredWrapper, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_bytes(self.magic)
		stream.write_uint(self.version)
		stream.write_uint(self.user_version)
		stream.write_type(self.root)
		stream.write_type(self.info)
		self.textures.write(stream, Texture, self.info.texture_count, None)
		stream.write_type(self.texture_wrapper)
		if self.root_1.flag == 3:
			stream.write_type(self.variant_wrapper)
		if self.root_1.flag == 2:
			stream.write_type(self.layered_wrapper)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MaterialcollectionInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* magic = {self.magic.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* user_version = {self.user_version.__repr__()}'
		s += f'\n	* root = {self.root.__repr__()}'
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* textures = {self.textures.__repr__()}'
		s += f'\n	* texture_wrapper = {self.texture_wrapper.__repr__()}'
		s += f'\n	* variant_wrapper = {self.variant_wrapper.__repr__()}'
		s += f'\n	* layered_wrapper = {self.layered_wrapper.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
