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

	_import_key = 'uimoviedefinition.compounds.UiMovieHeader'

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
		self.ui_triggers = Pointer(self.context, self.num_ui_triggers, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"])
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ui_names = Pointer(self.context, self.num_ui_names, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"])
		self.assetpkgs = Pointer(self.context, self.num_assetpkgs, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"])
		self.ptr_2 = Pointer(self.context, 0, None)
		self.list_1 = ArrayPointer(self.context, self.num_list_1, Uint)
		self.list_2 = ArrayPointer(self.context, self.num_list_2, Uint)
		self.ui_interfaces = Pointer(self.context, self.num_ui_interfaces, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"])
		self.ptr_3 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('movie_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('pkg_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('category_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('type_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('flag_1', Uint, (0, None), (False, None), (None, None))
		yield ('flag_2', Ushort, (0, None), (False, None), (None, None))
		yield ('flag_3', Ushort, (0, None), (False, None), (None, None))
		yield ('floats', Array, (0, None, (3,), Float), (False, None), (None, None))
		yield ('u_0', Ubyte, (0, None), (False, None), (None, None))
		yield ('num_ui_triggers', Ubyte, (0, None), (False, None), (None, None))
		yield ('u_1', Ubyte, (0, None), (False, None), (None, None))
		yield ('num_ui_names', Ubyte, (0, None), (False, None), (None, None))
		yield ('num_assetpkgs', Ubyte, (0, None), (False, None), (None, None))
		yield ('u_2', Ubyte, (0, None), (False, None), (None, None))
		yield ('num_list_1', Ubyte, (0, None), (False, None), (None, None))
		yield ('num_list_2', Ubyte, (0, None), (False, None), (None, None))
		yield ('num_ui_interfaces', Ubyte, (0, None), (False, None), (None, None))
		yield ('u_3', Ubyte, (0, None), (False, None), (None, None))
		yield ('u_4', Ubyte, (0, None), (False, None), (None, None))
		yield ('u_5', Ubyte, (0, None), (False, None), (None, None))
		yield ('ptr_0', Pointer, (0, None), (False, None), (None, None))
		yield ('ui_triggers', Pointer, (None, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None), (None, None))
		yield ('ptr_1', Pointer, (0, None), (False, None), (None, None))
		yield ('ui_names', Pointer, (None, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None), (None, None))
		yield ('assetpkgs', Pointer, (None, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None), (None, None))
		yield ('ptr_2', Pointer, (0, None), (False, None), (None, None))
		yield ('list_1', ArrayPointer, (None, Uint), (False, None), (None, None))
		yield ('list_2', ArrayPointer, (None, Uint), (False, None), (None, None))
		yield ('ui_interfaces', Pointer, (None, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None), (None, None))
		yield ('ptr_3', Pointer, (0, None), (False, None), (None, None))

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
		yield 'ui_triggers', Pointer, (instance.num_ui_triggers, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'ptr_1', Pointer, (0, None), (False, None)
		yield 'ui_names', Pointer, (instance.num_ui_names, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'assetpkgs', Pointer, (instance.num_assetpkgs, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'ptr_2', Pointer, (0, None), (False, None)
		yield 'list_1', ArrayPointer, (instance.num_list_1, Uint), (False, None)
		yield 'list_2', ArrayPointer, (instance.num_list_2, Uint), (False, None)
		yield 'ui_interfaces', Pointer, (instance.num_ui_interfaces, UiMovieHeader._import_map["uimoviedefinition.compounds.PtrList"]), (False, None)
		yield 'ptr_3', Pointer, (0, None), (False, None)


UiMovieHeader.init_attributes()
