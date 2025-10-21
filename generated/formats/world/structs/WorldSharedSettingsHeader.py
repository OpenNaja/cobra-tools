from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.world.imports import name_type_map


class WorldSharedSettingsHeader(MemStruct):

	__name__ = 'WorldSharedSettingsHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.world_type = name_type_map['Uint64'](self.context, 0, None)
		self.unknown = name_type_map['Uint64'](self.context, 0, None)

		# Name of the .biome file
		self.biome_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# .assetpkg file?
		self.skirt_package_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'biome_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'world_type', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'skirt_package_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'biome_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'world_type', name_type_map['Uint64'], (0, None), (False, None)
		yield 'skirt_package_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown', name_type_map['Uint64'], (0, None), (False, None)
