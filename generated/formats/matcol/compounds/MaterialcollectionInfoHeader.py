from generated.array import Array
from generated.formats.matcol.compounds.Layer import Layer
from generated.formats.matcol.compounds.MatcolRoot import MatcolRoot
from generated.formats.matcol.compounds.RootFrag import RootFrag
from generated.formats.matcol.compounds.Texture import Texture
from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader


class MaterialcollectionInfoHeader(GenericHeader):

	"""
	This reads a whole custom Matcol file
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.root = MatcolRoot(self.context, 0, None)
		self.info = RootFrag(self.context, 0, None)
		self.textures = Array((self.info.tex_count,), Texture, self.context, 0, None)
		self.layers = Array((self.info.mat_count,), Layer, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.root = MatcolRoot(self.context, 0, None)
		self.info = RootFrag(self.context, 0, None)
		self.textures = Array((self.info.tex_count,), Texture, self.context, 0, None)
		self.layers = Array((self.info.mat_count,), Layer, self.context, 0, None)

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
		instance.root = MatcolRoot.from_stream(stream, instance.context, 0, None)
		instance.info = RootFrag.from_stream(stream, instance.context, 0, None)
		instance.textures = Array.from_stream(stream, (instance.info.tex_count,), Texture, instance.context, 0, None)
		instance.layers = Array.from_stream(stream, (instance.info.mat_count,), Layer, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		MatcolRoot.to_stream(stream, instance.root)
		RootFrag.to_stream(stream, instance.info)
		Array.to_stream(stream, instance.textures, (instance.info.tex_count,), Texture, instance.context, 0, None)
		Array.to_stream(stream, instance.layers, (instance.info.mat_count,), Layer, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'root', MatcolRoot, (0, None)
		yield 'info', RootFrag, (0, None)
		yield 'textures', Array, ((instance.info.tex_count,), Texture, 0, None)
		yield 'layers', Array, ((instance.info.mat_count,), Layer, 0, None)

	def get_info_str(self, indent=0):
		return f'MaterialcollectionInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* root = {self.fmt_member(self.root, indent+1)}'
		s += f'\n	* info = {self.fmt_member(self.info, indent+1)}'
		s += f'\n	* textures = {self.fmt_member(self.textures, indent+1)}'
		s += f'\n	* layers = {self.fmt_member(self.layers, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
