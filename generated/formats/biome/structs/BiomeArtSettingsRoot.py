from generated.formats.biome.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BiomeArtSettingsRoot(MemStruct):

	__name__ = 'BiomeArtSettingsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.packages_to_load_count = name_type_map['Uint64'](self.context, 0, None)
		self.material_names_count = name_type_map['Uint64'](self.context, 0, None)
		self.material_icons_count = name_type_map['Uint64'](self.context, 0, None)
		self.packages_to_load = name_type_map['Pointer'](self.context, self.packages_to_load_count, name_type_map['ZStringList'])
		self.default_full_scale_material_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.material_names = name_type_map['Pointer'](self.context, self.material_names_count, name_type_map['ZStringList'])
		self.brush_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.brush_package = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.material_icons = name_type_map['ArrayPointer'](self.context, self.material_icons_count, name_type_map['BiomeArtIcon'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'packages_to_load', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'packages_to_load_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'default_full_scale_material_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'material_names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'material_names_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'brush_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'brush_package', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'material_icons', name_type_map['ArrayPointer'], (None, name_type_map['BiomeArtIcon']), (False, None), (None, None)
		yield 'material_icons_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'packages_to_load', name_type_map['Pointer'], (instance.packages_to_load_count, name_type_map['ZStringList']), (False, None)
		yield 'packages_to_load_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'default_full_scale_material_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'material_names', name_type_map['Pointer'], (instance.material_names_count, name_type_map['ZStringList']), (False, None)
		yield 'material_names_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'brush_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'brush_package', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'material_icons', name_type_map['ArrayPointer'], (instance.material_icons_count, name_type_map['BiomeArtIcon']), (False, None)
		yield 'material_icons_count', name_type_map['Uint64'], (0, None), (False, None)
