from generated.formats.assetpackobjectlists.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AssetPackObjectListsRoot(MemStruct):

	__name__ = 'AssetPackObjectListsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.asset_pack_object_lists_count = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pack_object_lists_list = name_type_map['ArrayPointer'](self.context, self.asset_pack_object_lists_count, name_type_map['AssetPackObjectList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'asset_pack_object_lists_list', name_type_map['ArrayPointer'], (None, name_type_map['AssetPackObjectList']), (False, None), (None, None)
		yield 'asset_pack_object_lists_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'asset_pack_object_lists_list', name_type_map['ArrayPointer'], (instance.asset_pack_object_lists_count, name_type_map['AssetPackObjectList']), (False, None)
		yield 'asset_pack_object_lists_count', name_type_map['Uint64'], (0, None), (False, None)
