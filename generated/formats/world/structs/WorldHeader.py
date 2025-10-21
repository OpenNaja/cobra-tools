from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.world.imports import name_type_map


class WorldHeader(MemStruct):

	__name__ = 'WorldHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.world_type = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pkgs_count = name_type_map['Uint64'](self.context, 0, None)
		self.prefabs_count = name_type_map['Uint64'](self.context, 0, None)
		self.asset_pkgs = name_type_map['Pointer'](self.context, self.asset_pkgs_count, name_type_map['ZStringList'])
		self.lua_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.ptr_0 = name_type_map['Pointer'](self.context, 0, None)
		self.ptr_1 = name_type_map['Pointer'](self.context, 0, None)
		self.prefabs = name_type_map['Pointer'](self.context, self.prefabs_count, name_type_map['ZStringList'])
		self.ptr_2 = name_type_map['Pointer'](self.context, 0, None)
		self.ptr_3 = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'world_type', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'asset_pkgs', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'asset_pkgs_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'lua_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'prefabs', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'ptr_2', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'prefabs_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ptr_3', name_type_map['Pointer'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'world_type', name_type_map['Uint64'], (0, None), (False, None)
		yield 'asset_pkgs', name_type_map['Pointer'], (instance.asset_pkgs_count, name_type_map['ZStringList']), (False, None)
		yield 'asset_pkgs_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'lua_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, None), (False, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, None), (False, None)
		yield 'prefabs', name_type_map['Pointer'], (instance.prefabs_count, name_type_map['ZStringList']), (False, None)
		yield 'ptr_2', name_type_map['Pointer'], (0, None), (False, None)
		yield 'prefabs_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ptr_3', name_type_map['Pointer'], (0, None), (False, None)
