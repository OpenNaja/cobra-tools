from generated.formats.assetpackobjectlists.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AssetPackObjectList(MemStruct):

	__name__ = 'AssetPackObjectList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.scenery_object_resource_count = name_type_map['Uint64'](self.context, 0, None)
		self.unit_count = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pack_object_list_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.scenery_object_resource_items = name_type_map['ArrayPointer'](self.context, self.scenery_object_resource_count, name_type_map['SceneryObjectResourceRef'])
		self.unit_items = name_type_map['ArrayPointer'](self.context, self.unit_count, name_type_map['UnitRef'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'asset_pack_object_list_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'scenery_object_resource_items', name_type_map['ArrayPointer'], (None, name_type_map['SceneryObjectResourceRef']), (False, None), (None, None)
		yield 'scenery_object_resource_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unit_items', name_type_map['ArrayPointer'], (None, name_type_map['UnitRef']), (False, None), (None, None)
		yield 'unit_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'asset_pack_object_list_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'scenery_object_resource_items', name_type_map['ArrayPointer'], (instance.scenery_object_resource_count, name_type_map['SceneryObjectResourceRef']), (False, None)
		yield 'scenery_object_resource_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unit_items', name_type_map['ArrayPointer'], (instance.unit_count, name_type_map['UnitRef']), (False, None)
		yield 'unit_count', name_type_map['Uint64'], (0, None), (False, None)
