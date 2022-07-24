from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.uimoviedefinition.compound.PtrList
import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class UiMovieHeader(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.floats = 0
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
		self.movie_name = 0
		self.pkg_name = 0
		self.category_name = 0
		self.type_name = 0
		self.ptr_0 = 0
		self.ui_triggers = 0
		self.ptr_1 = 0
		self.ui_names = 0
		self.assetpkgs = 0
		self.ptr_2 = 0
		self.list_1 = 0
		self.list_2 = 0
		self.ui_interfaces = 0
		self.ptr_3 = 0
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
		self.movie_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pkg_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.category_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.type_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ui_triggers = Pointer(self.context, self.num_ui_triggers, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ui_names = Pointer(self.context, self.num_ui_names, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
		self.assetpkgs = Pointer(self.context, self.num_assetpkgs, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.list_1 = ArrayPointer(self.context, self.num_list_1, generated.formats.base.basic.Uint)
		self.list_2 = ArrayPointer(self.context, self.num_list_2, generated.formats.base.basic.Uint)
		self.ui_interfaces = Pointer(self.context, self.num_ui_interfaces, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
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
		instance.movie_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.pkg_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.category_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.type_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
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
		instance.ui_triggers = Pointer.from_stream(stream, instance.context, instance.num_ui_triggers, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ui_names = Pointer.from_stream(stream, instance.context, instance.num_ui_names, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
		instance.assetpkgs = Pointer.from_stream(stream, instance.context, instance.num_assetpkgs, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.list_1 = ArrayPointer.from_stream(stream, instance.context, instance.num_list_1, generated.formats.base.basic.Uint)
		instance.list_2 = ArrayPointer.from_stream(stream, instance.context, instance.num_list_2, generated.formats.base.basic.Uint)
		instance.ui_interfaces = Pointer.from_stream(stream, instance.context, instance.num_ui_interfaces, generated.formats.uimoviedefinition.compound.PtrList.PtrList)
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.movie_name.arg = 0
		instance.pkg_name.arg = 0
		instance.category_name.arg = 0
		instance.type_name.arg = 0
		instance.ptr_0.arg = 0
		instance.ui_triggers.arg = instance.num_ui_triggers
		instance.ptr_1.arg = 0
		instance.ui_names.arg = instance.num_ui_names
		instance.assetpkgs.arg = instance.num_assetpkgs
		instance.ptr_2.arg = 0
		instance.list_1.arg = instance.num_list_1
		instance.list_2.arg = instance.num_list_2
		instance.ui_interfaces.arg = instance.num_ui_interfaces
		instance.ptr_3.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.movie_name)
		Pointer.to_stream(stream, instance.pkg_name)
		Pointer.to_stream(stream, instance.category_name)
		Pointer.to_stream(stream, instance.type_name)
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
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('movie_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('pkg_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('category_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('type_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('flag_1', Uint, (0, None))
		yield ('flag_2', Ushort, (0, None))
		yield ('flag_3', Ushort, (0, None))
		yield ('floats', Array, ((3,), Float, 0, None))
		yield ('u_0', Ubyte, (0, None))
		yield ('num_ui_triggers', Ubyte, (0, None))
		yield ('u_1', Ubyte, (0, None))
		yield ('num_ui_names', Ubyte, (0, None))
		yield ('num_assetpkgs', Ubyte, (0, None))
		yield ('u_2', Ubyte, (0, None))
		yield ('num_list_1', Ubyte, (0, None))
		yield ('num_list_2', Ubyte, (0, None))
		yield ('num_ui_interfaces', Ubyte, (0, None))
		yield ('u_3', Ubyte, (0, None))
		yield ('u_4', Ubyte, (0, None))
		yield ('u_5', Ubyte, (0, None))
		yield ('ptr_0', Pointer, (0, None))
		yield ('ui_triggers', Pointer, (instance.num_ui_triggers, generated.formats.uimoviedefinition.compound.PtrList.PtrList))
		yield ('ptr_1', Pointer, (0, None))
		yield ('ui_names', Pointer, (instance.num_ui_names, generated.formats.uimoviedefinition.compound.PtrList.PtrList))
		yield ('assetpkgs', Pointer, (instance.num_assetpkgs, generated.formats.uimoviedefinition.compound.PtrList.PtrList))
		yield ('ptr_2', Pointer, (0, None))
		yield ('list_1', ArrayPointer, (instance.num_list_1, generated.formats.base.basic.Uint))
		yield ('list_2', ArrayPointer, (instance.num_list_2, generated.formats.base.basic.Uint))
		yield ('ui_interfaces', Pointer, (instance.num_ui_interfaces, generated.formats.uimoviedefinition.compound.PtrList.PtrList))
		yield ('ptr_3', Pointer, (0, None))

	def get_info_str(self, indent=0):
		return f'UiMovieHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* movie_name = {fmt_member(self.movie_name, indent+1)}'
		s += f'\n	* pkg_name = {fmt_member(self.pkg_name, indent+1)}'
		s += f'\n	* category_name = {fmt_member(self.category_name, indent+1)}'
		s += f'\n	* type_name = {fmt_member(self.type_name, indent+1)}'
		s += f'\n	* flag_1 = {fmt_member(self.flag_1, indent+1)}'
		s += f'\n	* flag_2 = {fmt_member(self.flag_2, indent+1)}'
		s += f'\n	* flag_3 = {fmt_member(self.flag_3, indent+1)}'
		s += f'\n	* floats = {fmt_member(self.floats, indent+1)}'
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* num_ui_triggers = {fmt_member(self.num_ui_triggers, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* num_ui_names = {fmt_member(self.num_ui_names, indent+1)}'
		s += f'\n	* num_assetpkgs = {fmt_member(self.num_assetpkgs, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* num_list_1 = {fmt_member(self.num_list_1, indent+1)}'
		s += f'\n	* num_list_2 = {fmt_member(self.num_list_2, indent+1)}'
		s += f'\n	* num_ui_interfaces = {fmt_member(self.num_ui_interfaces, indent+1)}'
		s += f'\n	* u_3 = {fmt_member(self.u_3, indent+1)}'
		s += f'\n	* u_4 = {fmt_member(self.u_4, indent+1)}'
		s += f'\n	* u_5 = {fmt_member(self.u_5, indent+1)}'
		s += f'\n	* ptr_0 = {fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* ui_triggers = {fmt_member(self.ui_triggers, indent+1)}'
		s += f'\n	* ptr_1 = {fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* ui_names = {fmt_member(self.ui_names, indent+1)}'
		s += f'\n	* assetpkgs = {fmt_member(self.assetpkgs, indent+1)}'
		s += f'\n	* ptr_2 = {fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* list_1 = {fmt_member(self.list_1, indent+1)}'
		s += f'\n	* list_2 = {fmt_member(self.list_2, indent+1)}'
		s += f'\n	* ui_interfaces = {fmt_member(self.ui_interfaces, indent+1)}'
		s += f'\n	* ptr_3 = {fmt_member(self.ptr_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
