from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.world.imports import name_type_map


class WorldArtSettingsHeader(MemStruct):

	__name__ = 'WorldArtSettingsHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.size_x = name_type_map['Uint'](self.context, 0, None)
		self.size_y = name_type_map['Uint'](self.context, 0, None)
		self.size_z = name_type_map['Uint'](self.context, 0, None)
		self.unknown_1 = name_type_map['Uint'](self.context, 0, None)
		self.skirt_material_names_count = name_type_map['Uint64'](self.context, 0, None)
		self.packages_to_load_count = name_type_map['Uint64'](self.context, 0, None)
		self.unknown_3 = name_type_map['Uint64'](self.context, 0, None)
		self.sun_horizon_rotation = name_type_map['Float'](self.context, 0, None)
		self.sun_zenith_rotation = name_type_map['Float'](self.context, 0, None)
		self.moon_horizon_rotation = name_type_map['Float'](self.context, 0, None)
		self.moon_zenith_rotation = name_type_map['Float'](self.context, 0, None)
		self.skirt_resource_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.landscape_prefab_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# List of fgms for the skirts
		self.skirt_material_names = name_type_map['Pointer'](self.context, self.skirt_material_names_count, name_type_map['ZStringList'])
		self.packages_to_load = name_type_map['Pointer'](self.context, self.packages_to_load_count, name_type_map['ZStringList'])
		self.height_map_file_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.sea_prefab_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# Name of the LUT file to load for this world.
		self.colour_grade_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'size_x', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'size_y', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'size_z', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'skirt_resource_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'landscape_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'skirt_material_names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'skirt_material_names_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'packages_to_load', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'packages_to_load_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'height_map_file_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'sea_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'colour_grade_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'sun_horizon_rotation', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'sun_zenith_rotation', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'moon_horizon_rotation', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'moon_zenith_rotation', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'size_x', name_type_map['Uint'], (0, None), (False, None)
		yield 'size_y', name_type_map['Uint'], (0, None), (False, None)
		yield 'size_z', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'skirt_resource_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'landscape_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'skirt_material_names', name_type_map['Pointer'], (instance.skirt_material_names_count, name_type_map['ZStringList']), (False, None)
		yield 'skirt_material_names_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'packages_to_load', name_type_map['Pointer'], (instance.packages_to_load_count, name_type_map['ZStringList']), (False, None)
		yield 'packages_to_load_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'height_map_file_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'sea_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'colour_grade_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'sun_horizon_rotation', name_type_map['Float'], (0, None), (False, None)
		yield 'sun_zenith_rotation', name_type_map['Float'], (0, None), (False, None)
		yield 'moon_horizon_rotation', name_type_map['Float'], (0, None), (False, None)
		yield 'moon_zenith_rotation', name_type_map['Float'], (0, None), (False, None)
