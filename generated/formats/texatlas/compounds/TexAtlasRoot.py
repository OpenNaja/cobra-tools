from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TexAtlasRoot(MemStruct):

	__name__ = 'TexAtlasRoot'

	_import_key = 'texatlas.compounds.TexAtlasRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.texture_count = 0
		self.atlas_count = 0
		self.texture_list = ArrayPointer(self.context, self.texture_count, TexAtlasRoot._import_map["texatlas.compounds.TextureData"])
		self.atlas_list = ArrayPointer(self.context, self.atlas_count, TexAtlasRoot._import_map["texatlas.compounds.AtlasItem"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('texture_list', ArrayPointer, (None, TexAtlasRoot._import_map["texatlas.compounds.TextureData"]), (False, None), (None, None))
		yield ('texture_count', Uint64, (0, None), (False, None), (None, None))
		yield ('atlas_list', ArrayPointer, (None, TexAtlasRoot._import_map["texatlas.compounds.AtlasItem"]), (False, None), (None, None))
		yield ('atlas_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'texture_list', ArrayPointer, (instance.texture_count, TexAtlasRoot._import_map["texatlas.compounds.TextureData"]), (False, None)
		yield 'texture_count', Uint64, (0, None), (False, None)
		yield 'atlas_list', ArrayPointer, (instance.atlas_count, TexAtlasRoot._import_map["texatlas.compounds.AtlasItem"]), (False, None)
		yield 'atlas_count', Uint64, (0, None), (False, None)


TexAtlasRoot.init_attributes()
