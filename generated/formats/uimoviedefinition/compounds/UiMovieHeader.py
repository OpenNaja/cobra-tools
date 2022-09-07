import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class UiMovieHeader(MemStruct):

	__name__ = 'UiMovieHeader'

	_import_path = 'generated.formats.uimoviedefinition.compounds.UiMovieHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.floats = Array(self.context, 0, None, (0,), Float)
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
		self.movie_name = Pointer(self.context, 0, ZString)
		self.pkg_name = Pointer(self.context, 0, ZString)
		self.category_name = Pointer(self.context, 0, ZString)
		self.type_name = Pointer(self.context, 0, ZString)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ui_triggers = Pointer(self.context, self.num_ui_triggers, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ui_names = Pointer(self.context, self.num_ui_names, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.assetpkgs = Pointer(self.context, self.num_assetpkgs, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.ptr_2 = Pointer(self.context, 0, None)
		self.list_1 = ArrayPointer(self.context, self.num_list_1, Uint)
		self.list_2 = ArrayPointer(self.context, self.num_list_2, Uint)
		self.ui_interfaces = Pointer(self.context, self.num_ui_interfaces, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.ptr_3 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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
		self.movie_name = Pointer(self.context, 0, ZString)
		self.pkg_name = Pointer(self.context, 0, ZString)
		self.category_name = Pointer(self.context, 0, ZString)
		self.type_name = Pointer(self.context, 0, ZString)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ui_triggers = Pointer(self.context, self.num_ui_triggers, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ui_names = Pointer(self.context, self.num_ui_names, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.assetpkgs = Pointer(self.context, self.num_assetpkgs, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.ptr_2 = Pointer(self.context, 0, None)
		self.list_1 = ArrayPointer(self.context, self.num_list_1, Uint)
		self.list_2 = ArrayPointer(self.context, self.num_list_2, Uint)
		self.ui_interfaces = Pointer(self.context, self.num_ui_interfaces, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		self.ptr_3 = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.movie_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.pkg_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.category_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.type_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.flag_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.flag_2 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.flag_3 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (3,), Float)
		instance.u_0 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.num_ui_triggers = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.u_1 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.num_ui_names = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.num_assetpkgs = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.u_2 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.num_list_1 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.num_list_2 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.num_ui_interfaces = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.u_3 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.u_4 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.u_5 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ui_triggers = Pointer.from_stream(stream, instance.context, instance.num_ui_triggers, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ui_names = Pointer.from_stream(stream, instance.context, instance.num_ui_names, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		instance.assetpkgs = Pointer.from_stream(stream, instance.context, instance.num_assetpkgs, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.list_1 = ArrayPointer.from_stream(stream, instance.context, instance.num_list_1, Uint)
		instance.list_2 = ArrayPointer.from_stream(stream, instance.context, instance.num_list_2, Uint)
		instance.ui_interfaces = Pointer.from_stream(stream, instance.context, instance.num_ui_interfaces, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"])
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.movie_name, int):
			instance.movie_name.arg = 0
		if not isinstance(instance.pkg_name, int):
			instance.pkg_name.arg = 0
		if not isinstance(instance.category_name, int):
			instance.category_name.arg = 0
		if not isinstance(instance.type_name, int):
			instance.type_name.arg = 0
		if not isinstance(instance.ptr_0, int):
			instance.ptr_0.arg = 0
		if not isinstance(instance.ui_triggers, int):
			instance.ui_triggers.arg = instance.num_ui_triggers
		if not isinstance(instance.ptr_1, int):
			instance.ptr_1.arg = 0
		if not isinstance(instance.ui_names, int):
			instance.ui_names.arg = instance.num_ui_names
		if not isinstance(instance.assetpkgs, int):
			instance.assetpkgs.arg = instance.num_assetpkgs
		if not isinstance(instance.ptr_2, int):
			instance.ptr_2.arg = 0
		if not isinstance(instance.list_1, int):
			instance.list_1.arg = instance.num_list_1
		if not isinstance(instance.list_2, int):
			instance.list_2.arg = instance.num_list_2
		if not isinstance(instance.ui_interfaces, int):
			instance.ui_interfaces.arg = instance.num_ui_interfaces
		if not isinstance(instance.ptr_3, int):
			instance.ptr_3.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.movie_name)
		Pointer.to_stream(stream, instance.pkg_name)
		Pointer.to_stream(stream, instance.category_name)
		Pointer.to_stream(stream, instance.type_name)
		Uint.to_stream(stream, instance.flag_1)
		Ushort.to_stream(stream, instance.flag_2)
		Ushort.to_stream(stream, instance.flag_3)
		Array.to_stream(stream, instance.floats, instance.context, 0, None, (3,), Float)
		Ubyte.to_stream(stream, instance.u_0)
		Ubyte.to_stream(stream, instance.num_ui_triggers)
		Ubyte.to_stream(stream, instance.u_1)
		Ubyte.to_stream(stream, instance.num_ui_names)
		Ubyte.to_stream(stream, instance.num_assetpkgs)
		Ubyte.to_stream(stream, instance.u_2)
		Ubyte.to_stream(stream, instance.num_list_1)
		Ubyte.to_stream(stream, instance.num_list_2)
		Ubyte.to_stream(stream, instance.num_ui_interfaces)
		Ubyte.to_stream(stream, instance.u_3)
		Ubyte.to_stream(stream, instance.u_4)
		Ubyte.to_stream(stream, instance.u_5)
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.ui_triggers)
		Pointer.to_stream(stream, instance.ptr_1)
		Pointer.to_stream(stream, instance.ui_names)
		Pointer.to_stream(stream, instance.assetpkgs)
		Pointer.to_stream(stream, instance.ptr_2)
		ArrayPointer.to_stream(stream, instance.list_1)
		ArrayPointer.to_stream(stream, instance.list_2)
		Pointer.to_stream(stream, instance.ui_interfaces)
		Pointer.to_stream(stream, instance.ptr_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'movie_name', Pointer, (0, ZString), (False, None)
		yield 'pkg_name', Pointer, (0, ZString), (False, None)
		yield 'category_name', Pointer, (0, ZString), (False, None)
		yield 'type_name', Pointer, (0, ZString), (False, None)
		yield 'flag_1', Uint, (0, None), (False, None)
		yield 'flag_2', Ushort, (0, None), (False, None)
		yield 'flag_3', Ushort, (0, None), (False, None)
		yield 'floats', Array, (0, None, (3,), Float), (False, None)
		yield 'u_0', Ubyte, (0, None), (False, None)
		yield 'num_ui_triggers', Ubyte, (0, None), (False, None)
		yield 'u_1', Ubyte, (0, None), (False, None)
		yield 'num_ui_names', Ubyte, (0, None), (False, None)
		yield 'num_assetpkgs', Ubyte, (0, None), (False, None)
		yield 'u_2', Ubyte, (0, None), (False, None)
		yield 'num_list_1', Ubyte, (0, None), (False, None)
		yield 'num_list_2', Ubyte, (0, None), (False, None)
		yield 'num_ui_interfaces', Ubyte, (0, None), (False, None)
		yield 'u_3', Ubyte, (0, None), (False, None)
		yield 'u_4', Ubyte, (0, None), (False, None)
		yield 'u_5', Ubyte, (0, None), (False, None)
		yield 'ptr_0', Pointer, (0, None), (False, None)
		yield 'ui_triggers', Pointer, (instance.num_ui_triggers, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'ptr_1', Pointer, (0, None), (False, None)
		yield 'ui_names', Pointer, (instance.num_ui_names, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'assetpkgs', Pointer, (instance.num_assetpkgs, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'ptr_2', Pointer, (0, None), (False, None)
		yield 'list_1', ArrayPointer, (instance.num_list_1, Uint), (False, None)
		yield 'list_2', ArrayPointer, (instance.num_list_2, Uint), (False, None)
		yield 'ui_interfaces', Pointer, (instance.num_ui_interfaces, UiMovieHeader._import_path_map["generated.formats.uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'ptr_3', Pointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'UiMovieHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
