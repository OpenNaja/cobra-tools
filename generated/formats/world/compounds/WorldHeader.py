from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class WorldHeader(MemStruct):

	"""
	# NOTE, World struct in JWE1 has an extra pointer this import/export is not accounting for yet
	"""

	__name__ = 'WorldHeader'

	_import_path = 'generated.formats.world.compounds.WorldHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.world_type = 0
		self.asset_pkg_count = 0
		self.prefab_count = 0
		self.asset_pkgs = Pointer(self.context, self.asset_pkg_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"])
		self.lua_name = Pointer(self.context, 0, ZString)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.prefabs = Pointer(self.context, self.prefab_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"])
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.world_type = 0
		self.asset_pkg_count = 0
		self.prefab_count = 0
		self.asset_pkgs = Pointer(self.context, self.asset_pkg_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"])
		self.lua_name = Pointer(self.context, 0, ZString)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.prefabs = Pointer(self.context, self.prefab_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"])
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'world_type', Uint64, (0, None), (False, None)
		yield 'asset_pkgs', Pointer, (instance.asset_pkg_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"]), (False, None)
		yield 'asset_pkg_count', Uint64, (0, None), (False, None)
		yield 'lua_name', Pointer, (0, ZString), (False, None)
		yield 'ptr_0', Pointer, (0, None), (False, None)
		yield 'ptr_1', Pointer, (0, None), (False, None)
		yield 'prefabs', Pointer, (instance.prefab_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"]), (False, None)
		yield 'ptr_2', Pointer, (0, None), (False, None)
		yield 'prefab_count', Uint64, (0, None), (False, None)
		yield 'ptr_3', Pointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'WorldHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
