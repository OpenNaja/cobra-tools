import numpy
from generated.context import ContextReference
from generated.formats.ovl_base.compound.Pointer import Pointer


class UiMovieHeader:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.floats = numpy.zeros((3,), dtype=numpy.dtype('float32'))
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
		self.ptr_movie_name = Pointer(self.context, 0, None)
		self.ptr_pkg_name = Pointer(self.context, 0, None)
		self.ptr_category_name = Pointer(self.context, 0, None)
		self.ptr_type_name = Pointer(self.context, 0, None)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_ui_triggers = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_ui_names = Pointer(self.context, 0, None)
		self.ptr_assetpkgs = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_list_1 = Pointer(self.context, 0, None)
		self.ptr_list_2 = Pointer(self.context, 0, None)
		self.ptr_ui_interfaces = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.floats = numpy.zeros((3,), dtype=numpy.dtype('float32'))
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
		self.ptr_movie_name = Pointer(self.context, 0, None)
		self.ptr_pkg_name = Pointer(self.context, 0, None)
		self.ptr_category_name = Pointer(self.context, 0, None)
		self.ptr_type_name = Pointer(self.context, 0, None)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_ui_triggers = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_ui_names = Pointer(self.context, 0, None)
		self.ptr_assetpkgs = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_list_1 = Pointer(self.context, 0, None)
		self.ptr_list_2 = Pointer(self.context, 0, None)
		self.ptr_ui_interfaces = Pointer(self.context, 0, None)
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
		instance.ptr_movie_name = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_pkg_name = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_category_name = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_type_name = Pointer.from_stream(stream, instance.context, 0, None)
		instance.flag_1 = stream.read_uint()
		instance.flag_2 = stream.read_ushort()
		instance.flag_3 = stream.read_ushort()
		instance.floats = stream.read_floats((3,))
		instance.u_0 = stream.read_ubyte()
		instance.num_ui_triggers = stream.read_ubyte()
		instance.u_1 = stream.read_ubyte()
		instance.num_ui_names = stream.read_ubyte()
		instance.num_assetpkgs = stream.read_ubyte()
		instance.u_2 = stream.read_ubyte()
		instance.num_list_1 = stream.read_ubyte()
		instance.num_list_2 = stream.read_ubyte()
		instance.num_ui_interfaces = stream.read_ubyte()
		instance.u_3 = stream.read_ubyte()
		instance.u_4 = stream.read_ubyte()
		instance.u_5 = stream.read_ubyte()
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_ui_triggers = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_ui_names = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_assetpkgs = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_list_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_list_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_ui_interfaces = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_movie_name.arg = 0
		instance.ptr_pkg_name.arg = 0
		instance.ptr_category_name.arg = 0
		instance.ptr_type_name.arg = 0
		instance.ptr_0.arg = 0
		instance.ptr_ui_triggers.arg = 0
		instance.ptr_1.arg = 0
		instance.ptr_ui_names.arg = 0
		instance.ptr_assetpkgs.arg = 0
		instance.ptr_2.arg = 0
		instance.ptr_list_1.arg = 0
		instance.ptr_list_2.arg = 0
		instance.ptr_ui_interfaces.arg = 0
		instance.ptr_3.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		Pointer.to_stream(stream, instance.ptr_movie_name)
		Pointer.to_stream(stream, instance.ptr_pkg_name)
		Pointer.to_stream(stream, instance.ptr_category_name)
		Pointer.to_stream(stream, instance.ptr_type_name)
		stream.write_uint(instance.flag_1)
		stream.write_ushort(instance.flag_2)
		stream.write_ushort(instance.flag_3)
		stream.write_floats(instance.floats)
		stream.write_ubyte(instance.u_0)
		stream.write_ubyte(instance.num_ui_triggers)
		stream.write_ubyte(instance.u_1)
		stream.write_ubyte(instance.num_ui_names)
		stream.write_ubyte(instance.num_assetpkgs)
		stream.write_ubyte(instance.u_2)
		stream.write_ubyte(instance.num_list_1)
		stream.write_ubyte(instance.num_list_2)
		stream.write_ubyte(instance.num_ui_interfaces)
		stream.write_ubyte(instance.u_3)
		stream.write_ubyte(instance.u_4)
		stream.write_ubyte(instance.u_5)
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.ptr_ui_triggers)
		Pointer.to_stream(stream, instance.ptr_1)
		Pointer.to_stream(stream, instance.ptr_ui_names)
		Pointer.to_stream(stream, instance.ptr_assetpkgs)
		Pointer.to_stream(stream, instance.ptr_2)
		Pointer.to_stream(stream, instance.ptr_list_1)
		Pointer.to_stream(stream, instance.ptr_list_2)
		Pointer.to_stream(stream, instance.ptr_ui_interfaces)
		Pointer.to_stream(stream, instance.ptr_3)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

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
