from generated.formats.assetpackobjectlists.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AssetPackObjectList(MemStruct):

	__name__ = 'AssetPackObjectList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.asset_pack_object_list_count = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pack_object_list_unknown_1 = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pack_object_list_unknown_2 = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pack_object_list_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.asset_pack_object_list_items = name_type_map['ArrayPointer'](self.context, self.asset_pack_object_list_count, name_type_map['AssetPackObject'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'asset_pack_object_list_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'asset_pack_object_list_items', name_type_map['ArrayPointer'], (None, name_type_map['AssetPackObject']), (False, None), (None, None)
		yield 'asset_pack_object_list_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'asset_pack_object_list_unknown_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'asset_pack_object_list_unknown_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'asset_pack_object_list_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'asset_pack_object_list_items', name_type_map['ArrayPointer'], (instance.asset_pack_object_list_count, name_type_map['AssetPackObject']), (False, None)
		yield 'asset_pack_object_list_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'asset_pack_object_list_unknown_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'asset_pack_object_list_unknown_2', name_type_map['Uint64'], (0, None), (False, None)
