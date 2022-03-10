from generated.context import ContextReference
from generated.formats.world.compound.Pointer import Pointer


class WorldHeader:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.world_type = 0
		self.ptr_asset_pkg = Pointer(self.context, None, None)
		self.asset_pkg_count = 0
		self.ptr_lua = Pointer(self.context, None, None)
		self.ptr_0 = Pointer(self.context, None, None)
		self.ptr_1 = Pointer(self.context, None, None)
		self.ptr_prefab = Pointer(self.context, None, None)
		self.ptr_2 = Pointer(self.context, None, None)
		self.prefab_count = 0
		self.ptr_3 = Pointer(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.world_type = 0
		self.ptr_asset_pkg = Pointer(self.context, None, None)
		self.asset_pkg_count = 0
		self.ptr_lua = Pointer(self.context, None, None)
		self.ptr_0 = Pointer(self.context, None, None)
		self.ptr_1 = Pointer(self.context, None, None)
		self.ptr_prefab = Pointer(self.context, None, None)
		self.ptr_2 = Pointer(self.context, None, None)
		self.prefab_count = 0
		self.ptr_3 = Pointer(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.world_type = stream.read_uint64()
		self.ptr_asset_pkg = stream.read_type(Pointer, (self.context, None, None))
		self.asset_pkg_count = stream.read_uint64()
		self.ptr_lua = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_0 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_1 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_prefab = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_2 = stream.read_type(Pointer, (self.context, None, None))
		self.prefab_count = stream.read_uint64()
		self.ptr_3 = stream.read_type(Pointer, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.world_type)
		stream.write_type(self.ptr_asset_pkg)
		stream.write_uint64(self.asset_pkg_count)
		stream.write_type(self.ptr_lua)
		stream.write_type(self.ptr_0)
		stream.write_type(self.ptr_1)
		stream.write_type(self.ptr_prefab)
		stream.write_type(self.ptr_2)
		stream.write_uint64(self.prefab_count)
		stream.write_type(self.ptr_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'WorldHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* world_type = {self.world_type.__repr__()}'
		s += f'\n	* ptr_asset_pkg = {self.ptr_asset_pkg.__repr__()}'
		s += f'\n	* asset_pkg_count = {self.asset_pkg_count.__repr__()}'
		s += f'\n	* ptr_lua = {self.ptr_lua.__repr__()}'
		s += f'\n	* ptr_0 = {self.ptr_0.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* ptr_prefab = {self.ptr_prefab.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		s += f'\n	* prefab_count = {self.prefab_count.__repr__()}'
		s += f'\n	* ptr_3 = {self.ptr_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
