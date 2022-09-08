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

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'mat_type', Uint64, (0, None), (False, None)
		yield 'textures', ArrayPointer, (instance.tex_count, RootFrag._import_path_map["generated.formats.matcol.compounds.Texture"]), (False, None)
		yield 'tex_count', Uint64, (0, None), (False, None)
		yield 'materials', ArrayPointer, (instance.mat_count, RootFrag._import_path_map["generated.formats.matcol.compounds.LayerFrag"]), (False, None)
		yield 'mat_count', Uint64, (0, None), (False, None)
		yield 'unk', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'RootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
