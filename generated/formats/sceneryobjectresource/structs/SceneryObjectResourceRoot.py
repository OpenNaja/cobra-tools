from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.sceneryobjectresource.imports import name_type_map


class SceneryObjectResourceRoot(MemStruct):

	__name__ = 'SceneryObjectResourceRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.faction_tags_count = name_type_map['Uint64'](self.context, 0, None)
		self.resource_types_tags_count = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pack_tags_count = name_type_map['Uint64'](self.context, 0, None)
		self.primary_group_tags_count = name_type_map['Uint64'](self.context, 0, None)
		self.secondary_group_tags_count = name_type_map['Uint64'](self.context, 0, None)
		self.functional_tags_count = name_type_map['Uint64'](self.context, 0, None)
		self.unk_0 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_1 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_2 = name_type_map['Uint'](self.context, 0, None)
		self.unk_3 = name_type_map['Uint'](self.context, 0, None)
		self.variant_names_count = name_type_map['Uint64'](self.context, 0, None)
		self.unk_4 = name_type_map['Uint64'](self.context, 0, None)
		self.faction_tags = name_type_map['Pointer'](self.context, self.faction_tags_count, name_type_map['ZStringList'])

		# main biome
		self.resource_types_tags = name_type_map['Pointer'](self.context, self.resource_types_tags_count, name_type_map['ZStringList'])
		self.asset_pack_tags = name_type_map['Pointer'](self.context, self.asset_pack_tags_count, name_type_map['ZStringList'])
		self.primary_group_tags = name_type_map['Pointer'](self.context, self.primary_group_tags_count, name_type_map['ZStringList'])
		self.secondary_group_tags = name_type_map['Pointer'](self.context, self.secondary_group_tags_count, name_type_map['ZStringList'])
		self.functional_tags = name_type_map['Pointer'](self.context, self.functional_tags_count, name_type_map['ZStringList'])
		self.variant_names = name_type_map['Pointer'](self.context, self.variant_names_count, name_type_map['ZStringList'])
		self.child_scenery_resource_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.parent_scenery_resource_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'faction_tags', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'faction_tags_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'resource_types_tags', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'resource_types_tags_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'asset_pack_tags', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'asset_pack_tags_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'primary_group_tags', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'primary_group_tags_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'secondary_group_tags', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'secondary_group_tags_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'functional_tags', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'functional_tags_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'variant_names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'variant_names_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'child_scenery_resource_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'parent_scenery_resource_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_4', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'faction_tags', name_type_map['Pointer'], (instance.faction_tags_count, name_type_map['ZStringList']), (False, None)
		yield 'faction_tags_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'resource_types_tags', name_type_map['Pointer'], (instance.resource_types_tags_count, name_type_map['ZStringList']), (False, None)
		yield 'resource_types_tags_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'asset_pack_tags', name_type_map['Pointer'], (instance.asset_pack_tags_count, name_type_map['ZStringList']), (False, None)
		yield 'asset_pack_tags_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'primary_group_tags', name_type_map['Pointer'], (instance.primary_group_tags_count, name_type_map['ZStringList']), (False, None)
		yield 'primary_group_tags_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'secondary_group_tags', name_type_map['Pointer'], (instance.secondary_group_tags_count, name_type_map['ZStringList']), (False, None)
		yield 'secondary_group_tags_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'functional_tags', name_type_map['Pointer'], (instance.functional_tags_count, name_type_map['ZStringList']), (False, None)
		yield 'functional_tags_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'variant_names', name_type_map['Pointer'], (instance.variant_names_count, name_type_map['ZStringList']), (False, None)
		yield 'variant_names_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'child_scenery_resource_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'parent_scenery_resource_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_4', name_type_map['Uint64'], (0, None), (False, None)
