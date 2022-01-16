import numpy
import typing
from generated.array import Array
from generated.formats.matcol.compound.Layer import Layer
from generated.formats.matcol.compound.MatcolRoot import MatcolRoot
from generated.formats.matcol.compound.RootFrag import RootFrag
from generated.formats.matcol.compound.Texture import Texture
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class MaterialcollectionInfoHeader(GenericHeader):

	"""
	This reads a whole custom Matcol file
	"""

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.root = MatcolRoot(self.context, None, None)
		self.info = RootFrag(self.context, None, None)
		self.textures = Array(self.context)
		self.layers = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.root = MatcolRoot(self.context, None, None)
		self.info = RootFrag(self.context, None, None)
		self.textures = Array(self.context)
		self.layers = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.root = stream.read_type(MatcolRoot, (self.context, None, None))
		self.info = stream.read_type(RootFrag, (self.context, None, None))
		self.textures.read(stream, Texture, self.info.tex_count, None)
		self.layers.read(stream, Layer, self.info.mat_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_type(self.root)
		stream.write_type(self.info)
		self.textures.write(stream, Texture, self.info.tex_count, None)
		self.layers.write(stream, Layer, self.info.mat_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MaterialcollectionInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* root = {self.root.__repr__()}'
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* textures = {self.textures.__repr__()}'
		s += f'\n	* layers = {self.layers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
