from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.world.compound.PtrList
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class WorldHeader(MemStruct):

	"""
	# NOTE, World struct in JWE1 has an extra pointer this import/export is not accounting for yet
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.world_type = 0
		self.asset_pkg_count = 0
		self.prefab_count = 0
		self.asset_pkgs = 0
		self.lua_name = 0
		self.ptr_0 = 0
		self.ptr_1 = 0
		self.prefabs = 0
		self.ptr_2 = 0
		self.ptr_3 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.world_type = 0
		self.asset_pkg_count = 0
		self.prefab_count = 0
		self.asset_pkgs = Pointer(self.context, self.asset_pkg_count, generated.formats.world.compound.PtrList.PtrList)
		self.lua_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.prefabs = Pointer(self.context, self.prefab_count, generated.formats.world.compound.PtrList.PtrList)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.world_type = stream.read_uint64()
		instance.asset_pkgs = Pointer.from_stream(stream, instance.context, instance.asset_pkg_count, generated.formats.world.compound.PtrList.PtrList)
		instance.asset_pkg_count = stream.read_uint64()
		instance.lua_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.prefabs = Pointer.from_stream(stream, instance.context, instance.prefab_count, generated.formats.world.compound.PtrList.PtrList)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.prefab_count = stream.read_uint64()
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.asset_pkgs.arg = instance.asset_pkg_count
		instance.lua_name.arg = 0
		instance.ptr_0.arg = 0
		instance.ptr_1.arg = 0
		instance.prefabs.arg = instance.prefab_count
		instance.ptr_2.arg = 0
		instance.ptr_3.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.world_type)
		Pointer.to_stream(stream, instance.asset_pkgs)
		stream.write_uint64(instance.asset_pkg_count)
		Pointer.to_stream(stream, instance.lua_name)
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.ptr_1)
		Pointer.to_stream(stream, instance.prefabs)
		Pointer.to_stream(stream, instance.ptr_2)
		stream.write_uint64(instance.prefab_count)
		Pointer.to_stream(stream, instance.ptr_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('world_type', Uint64, (0, None))
		yield ('asset_pkgs', Pointer, (instance.asset_pkg_count, generated.formats.world.compound.PtrList.PtrList))
		yield ('asset_pkg_count', Uint64, (0, None))
		yield ('lua_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('ptr_0', Pointer, (0, None))
		yield ('ptr_1', Pointer, (0, None))
		yield ('prefabs', Pointer, (instance.prefab_count, generated.formats.world.compound.PtrList.PtrList))
		yield ('ptr_2', Pointer, (0, None))
		yield ('prefab_count', Uint64, (0, None))
		yield ('ptr_3', Pointer, (0, None))

	def get_info_str(self, indent=0):
		return f'WorldHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* world_type = {fmt_member(self.world_type, indent+1)}'
		s += f'\n	* asset_pkgs = {fmt_member(self.asset_pkgs, indent+1)}'
		s += f'\n	* asset_pkg_count = {fmt_member(self.asset_pkg_count, indent+1)}'
		s += f'\n	* lua_name = {fmt_member(self.lua_name, indent+1)}'
		s += f'\n	* ptr_0 = {fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* ptr_1 = {fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* prefabs = {fmt_member(self.prefabs, indent+1)}'
		s += f'\n	* ptr_2 = {fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* prefab_count = {fmt_member(self.prefab_count, indent+1)}'
		s += f'\n	* ptr_3 = {fmt_member(self.ptr_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
