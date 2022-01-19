import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.uimoviedefinition.compound.Pointer import Pointer


class UiMovieHeader:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ptr_movie_name = Pointer(self.context, None, None)
		self.ptr_pkg_name = Pointer(self.context, None, None)
		self.ptr_category_name = Pointer(self.context, None, None)
		self.ptr_type_name = Pointer(self.context, None, None)
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.floats = numpy.zeros((3), dtype='float')
		self.u_0 = 0
		self.num_ui_triggers = 0
		self.u_1 = 0
		self.num_ui_names = 0
		self.num_assetpkgs = 0
		self.u_2 = 0
		self.num_list_1 = 0
		self.num_list_2 = 0
		self.num_ui_interfaces = 0
		self.u_3 = 0
		self.u_4 = 0
		self.u_5 = 0
		self.ptr_0 = Pointer(self.context, None, None)
		self.ptr_ui_triggers = Pointer(self.context, None, None)
		self.ptr_1 = Pointer(self.context, None, None)
		self.ptr_ui_names = Pointer(self.context, None, None)
		self.ptr_assetpkgs = Pointer(self.context, None, None)
		self.ptr_2 = Pointer(self.context, None, None)
		self.ptr_list_1 = Pointer(self.context, None, None)
		self.ptr_list_2 = Pointer(self.context, None, None)
		self.ptr_ui_interfaces = Pointer(self.context, None, None)
		self.ptr_3 = Pointer(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.ptr_movie_name = Pointer(self.context, None, None)
		self.ptr_pkg_name = Pointer(self.context, None, None)
		self.ptr_category_name = Pointer(self.context, None, None)
		self.ptr_type_name = Pointer(self.context, None, None)
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.floats = numpy.zeros((3), dtype='float')
		self.u_0 = 0
		self.num_ui_triggers = 0
		self.u_1 = 0
		self.num_ui_names = 0
		self.num_assetpkgs = 0
		self.u_2 = 0
		self.num_list_1 = 0
		self.num_list_2 = 0
		self.num_ui_interfaces = 0
		self.u_3 = 0
		self.u_4 = 0
		self.u_5 = 0
		self.ptr_0 = Pointer(self.context, None, None)
		self.ptr_ui_triggers = Pointer(self.context, None, None)
		self.ptr_1 = Pointer(self.context, None, None)
		self.ptr_ui_names = Pointer(self.context, None, None)
		self.ptr_assetpkgs = Pointer(self.context, None, None)
		self.ptr_2 = Pointer(self.context, None, None)
		self.ptr_list_1 = Pointer(self.context, None, None)
		self.ptr_list_2 = Pointer(self.context, None, None)
		self.ptr_ui_interfaces = Pointer(self.context, None, None)
		self.ptr_3 = Pointer(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.ptr_movie_name = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_pkg_name = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_category_name = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_type_name = stream.read_type(Pointer, (self.context, None, None))
		self.flag_1 = stream.read_uint()
		self.flag_2 = stream.read_ushort()
		self.flag_3 = stream.read_ushort()
		self.floats = stream.read_floats((3))
		self.u_0 = stream.read_ubyte()
		self.num_ui_triggers = stream.read_ubyte()
		self.u_1 = stream.read_ubyte()
		self.num_ui_names = stream.read_ubyte()
		self.num_assetpkgs = stream.read_ubyte()
		self.u_2 = stream.read_ubyte()
		self.num_list_1 = stream.read_ubyte()
		self.num_list_2 = stream.read_ubyte()
		self.num_ui_interfaces = stream.read_ubyte()
		self.u_3 = stream.read_ubyte()
		self.u_4 = stream.read_ubyte()
		self.u_5 = stream.read_ubyte()
		self.ptr_0 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_ui_triggers = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_1 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_ui_names = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_assetpkgs = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_2 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_list_1 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_list_2 = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_ui_interfaces = stream.read_type(Pointer, (self.context, None, None))
		self.ptr_3 = stream.read_type(Pointer, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.ptr_movie_name)
		stream.write_type(self.ptr_pkg_name)
		stream.write_type(self.ptr_category_name)
		stream.write_type(self.ptr_type_name)
		stream.write_uint(self.flag_1)
		stream.write_ushort(self.flag_2)
		stream.write_ushort(self.flag_3)
		stream.write_floats(self.floats)
		stream.write_ubyte(self.u_0)
		stream.write_ubyte(self.num_ui_triggers)
		stream.write_ubyte(self.u_1)
		stream.write_ubyte(self.num_ui_names)
		stream.write_ubyte(self.num_assetpkgs)
		stream.write_ubyte(self.u_2)
		stream.write_ubyte(self.num_list_1)
		stream.write_ubyte(self.num_list_2)
		stream.write_ubyte(self.num_ui_interfaces)
		stream.write_ubyte(self.u_3)
		stream.write_ubyte(self.u_4)
		stream.write_ubyte(self.u_5)
		stream.write_type(self.ptr_0)
		stream.write_type(self.ptr_ui_triggers)
		stream.write_type(self.ptr_1)
		stream.write_type(self.ptr_ui_names)
		stream.write_type(self.ptr_assetpkgs)
		stream.write_type(self.ptr_2)
		stream.write_type(self.ptr_list_1)
		stream.write_type(self.ptr_list_2)
		stream.write_type(self.ptr_ui_interfaces)
		stream.write_type(self.ptr_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'UiMovieHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ptr_movie_name = {self.ptr_movie_name.__repr__()}'
		s += f'\n	* ptr_pkg_name = {self.ptr_pkg_name.__repr__()}'
		s += f'\n	* ptr_category_name = {self.ptr_category_name.__repr__()}'
		s += f'\n	* ptr_type_name = {self.ptr_type_name.__repr__()}'
		s += f'\n	* flag_1 = {self.flag_1.__repr__()}'
		s += f'\n	* flag_2 = {self.flag_2.__repr__()}'
		s += f'\n	* flag_3 = {self.flag_3.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* u_0 = {self.u_0.__repr__()}'
		s += f'\n	* num_ui_triggers = {self.num_ui_triggers.__repr__()}'
		s += f'\n	* u_1 = {self.u_1.__repr__()}'
		s += f'\n	* num_ui_names = {self.num_ui_names.__repr__()}'
		s += f'\n	* num_assetpkgs = {self.num_assetpkgs.__repr__()}'
		s += f'\n	* u_2 = {self.u_2.__repr__()}'
		s += f'\n	* num_list_1 = {self.num_list_1.__repr__()}'
		s += f'\n	* num_list_2 = {self.num_list_2.__repr__()}'
		s += f'\n	* num_ui_interfaces = {self.num_ui_interfaces.__repr__()}'
		s += f'\n	* u_3 = {self.u_3.__repr__()}'
		s += f'\n	* u_4 = {self.u_4.__repr__()}'
		s += f'\n	* u_5 = {self.u_5.__repr__()}'
		s += f'\n	* ptr_0 = {self.ptr_0.__repr__()}'
		s += f'\n	* ptr_ui_triggers = {self.ptr_ui_triggers.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* ptr_ui_names = {self.ptr_ui_names.__repr__()}'
		s += f'\n	* ptr_assetpkgs = {self.ptr_assetpkgs.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		s += f'\n	* ptr_list_1 = {self.ptr_list_1.__repr__()}'
		s += f'\n	* ptr_list_2 = {self.ptr_list_2.__repr__()}'
		s += f'\n	* ptr_ui_interfaces = {self.ptr_ui_interfaces.__repr__()}'
		s += f'\n	* ptr_3 = {self.ptr_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
