from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RootFrag(MemStruct):

	"""
	first frag data
	(3=variant, 2=layered)
	"""

	__name__ = 'RootFrag'

	_import_path = 'generated.formats.matcol.compounds.RootFrag'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mat_type = 0
		self.tex_count = 0
		self.mat_count = 0
		self.unk = 0
		self.textures = ArrayPointer(self.context, self.tex_count, RootFrag._import_path_map["generated.formats.matcol.compounds.Texture"])
		self.materials = ArrayPointer(self.context, self.mat_count, RootFrag._import_path_map["generated.formats.matcol.compounds.LayerFrag"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.mat_type = 0
		self.tex_count = 0
		self.mat_count = 0
		self.unk = 0
		self.textures = ArrayPointer(self.context, self.tex_count, RootFrag._import_path_map["generated.formats.matcol.compounds.Texture"])
		self.materials = ArrayPointer(self.context, self.mat_count, RootFrag._import_path_map["generated.formats.matcol.compounds.LayerFrag"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.mat_type = Uint64.from_stream(stream, instance.context, 0, None)
		instance.textures = ArrayPointer.from_stream(stream, instance.context, instance.tex_count, RootFrag._import_path_map["generated.formats.matcol.compounds.Texture"])
		instance.tex_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.materials = ArrayPointer.from_stream(stream, instance.context, instance.mat_count, RootFrag._import_path_map["generated.formats.matcol.compounds.LayerFrag"])
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
		yield 'mat_type', Uint64, (0, None), (False, None)
		yield 'textures', ArrayPointer, (instance.tex_count, RootFrag._import_path_map["generated.formats.matcol.compounds.Texture"]), (False, None)
		yield 'tex_count', Uint64, (0, None), (False, None)
		yield 'materials', ArrayPointer, (instance.mat_count, RootFrag._import_path_map["generated.formats.matcol.compounds.LayerFrag"]), (False, None)
		yield 'mat_count', Uint64, (0, None), (False, None)
		yield 'unk', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'RootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
