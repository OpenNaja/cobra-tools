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
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.world_type = Uint64.from_stream(stream, instance.context, 0, None)
		instance.asset_pkgs = Pointer.from_stream(stream, instance.context, instance.asset_pkg_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"])
		instance.asset_pkg_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.lua_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.prefabs = Pointer.from_stream(stream, instance.context, instance.prefab_count, WorldHeader._import_path_map["generated.formats.world.compounds.PtrList"])
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.prefab_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.asset_pkgs, int):
			instance.asset_pkgs.arg = instance.asset_pkg_count
		if not isinstance(instance.lua_name, int):
			instance.lua_name.arg = 0
		if not isinstance(instance.ptr_0, int):
			instance.ptr_0.arg = 0
		if not isinstance(instance.ptr_1, int):
			instance.ptr_1.arg = 0
		if not isinstance(instance.prefabs, int):
			instance.prefabs.arg = instance.prefab_count
		if not isinstance(instance.ptr_2, int):
			instance.ptr_2.arg = 0
		if not isinstance(instance.ptr_3, int):
			instance.ptr_3.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.world_type)
		Pointer.to_stream(stream, instance.asset_pkgs)
		Uint64.to_stream(stream, instance.asset_pkg_count)
		Pointer.to_stream(stream, instance.lua_name)
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.ptr_1)
		Pointer.to_stream(stream, instance.prefabs)
		Pointer.to_stream(stream, instance.ptr_2)
		Uint64.to_stream(stream, instance.prefab_count)
		Pointer.to_stream(stream, instance.ptr_3)

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
