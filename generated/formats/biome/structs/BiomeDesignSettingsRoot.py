from generated.formats.biome.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BiomeDesignSettingsRoot(MemStruct):

	__name__ = 'BiomeDesignSettingsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.sandbox_initial_save_relative_file_path = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.sandbox_world_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'sandbox_initial_save_relative_file_path', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'sandbox_world_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'sandbox_initial_save_relative_file_path', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'sandbox_world_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
