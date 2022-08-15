import generated.formats.matcol.compounds.LayerFrag
import generated.formats.matcol.compounds.Texture
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RootFrag(MemStruct):

	"""
	first frag data
	(3=variant, 2=layered)
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mat_type = 0
		self.tex_count = 0
		self.mat_count = 0
		self.unk = 0
		self.textures = ArrayPointer(self.context, self.tex_count, generated.formats.matcol.compounds.Texture.Texture)
		self.materials = ArrayPointer(self.context, self.mat_count, generated.formats.matcol.compounds.LayerFrag.LayerFrag)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.mat_type = 0
		self.tex_count = 0
		self.mat_count = 0
		self.unk = 0
		self.textures = ArrayPointer(self.context, self.tex_count, generated.formats.matcol.compounds.Texture.Texture)
		self.materials = ArrayPointer(self.context, self.mat_count, generated.formats.matcol.compounds.LayerFrag.LayerFrag)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.mat_type = Uint64.from_stream(stream, instance.context, 0, None)
		instance.textures = ArrayPointer.from_stream(stream, instance.context, instance.tex_count, generated.formats.matcol.compounds.Texture.Texture)
		instance.tex_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.materials = ArrayPointer.from_stream(stream, instance.context, instance.mat_count, generated.formats.matcol.compounds.LayerFrag.LayerFrag)
		instance.mat_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.textures, int):
			instance.textures.arg = instance.tex_count
		if not isinstance(instance.materials, int):
			instance.materials.arg = instance.mat_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.mat_type)
		ArrayPointer.to_stream(stream, instance.textures)
		Uint64.to_stream(stream, instance.tex_count)
		ArrayPointer.to_stream(stream, instance.materials)
		Uint64.to_stream(stream, instance.mat_count)
		Uint64.to_stream(stream, instance.unk)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'mat_type', Uint64, (0, None)
		yield 'textures', ArrayPointer, (instance.tex_count, generated.formats.matcol.compounds.Texture.Texture)
		yield 'tex_count', Uint64, (0, None)
		yield 'materials', ArrayPointer, (instance.mat_count, generated.formats.matcol.compounds.LayerFrag.LayerFrag)
		yield 'mat_count', Uint64, (0, None)
		yield 'unk', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'RootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* mat_type = {self.fmt_member(self.mat_type, indent+1)}'
		s += f'\n	* textures = {self.fmt_member(self.textures, indent+1)}'
		s += f'\n	* tex_count = {self.fmt_member(self.tex_count, indent+1)}'
		s += f'\n	* materials = {self.fmt_member(self.materials, indent+1)}'
		s += f'\n	* mat_count = {self.fmt_member(self.mat_count, indent+1)}'
		s += f'\n	* unk = {self.fmt_member(self.unk, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
