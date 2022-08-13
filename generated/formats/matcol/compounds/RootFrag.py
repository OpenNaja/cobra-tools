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
		instance.mat_type = stream.read_uint64()
		instance.textures = ArrayPointer.from_stream(stream, instance.context, instance.tex_count, generated.formats.matcol.compounds.Texture.Texture)
		instance.tex_count = stream.read_uint64()
		instance.materials = ArrayPointer.from_stream(stream, instance.context, instance.mat_count, generated.formats.matcol.compounds.LayerFrag.LayerFrag)
		instance.mat_count = stream.read_uint64()
		instance.unk = stream.read_uint64()
		if not isinstance(instance.textures, int):
			instance.textures.arg = instance.tex_count
		if not isinstance(instance.materials, int):
			instance.materials.arg = instance.mat_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.mat_type)
		ArrayPointer.to_stream(stream, instance.textures)
		stream.write_uint64(instance.tex_count)
		ArrayPointer.to_stream(stream, instance.materials)
		stream.write_uint64(instance.mat_count)
		stream.write_uint64(instance.unk)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('mat_type', Uint64, (0, None))
		yield ('textures', ArrayPointer, (instance.tex_count, generated.formats.matcol.compounds.Texture.Texture))
		yield ('tex_count', Uint64, (0, None))
		yield ('materials', ArrayPointer, (instance.mat_count, generated.formats.matcol.compounds.LayerFrag.LayerFrag))
		yield ('mat_count', Uint64, (0, None))
		yield ('unk', Uint64, (0, None))

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
