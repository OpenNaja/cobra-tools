import generated.formats.specdef.compounds.DataPtr
import generated.formats.specdef.compounds.NamePtr
import generated.formats.specdef.compounds.PtrList
import generated.formats.specdef.compounds.Spec
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SpecdefRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.attrib_count = 0
		self.flags = 0
		self.name_count = 0
		self.childspec_count = 0
		self.manager_count = 0
		self.script_count = 0
		self.attribs = ArrayPointer(self.context, self.attrib_count, generated.formats.specdef.compounds.Spec.Spec)
		self.name_foreach_attribs = ForEachPointer(self.context, self.attribs, generated.formats.specdef.compounds.NamePtr.NamePtr)
		self.data_foreach_attribs = ForEachPointer(self.context, self.attribs, generated.formats.specdef.compounds.DataPtr.DataPtr)
		self.names = Pointer(self.context, self.name_count, generated.formats.specdef.compounds.PtrList.PtrList)
		self.childspecs = Pointer(self.context, self.childspec_count, generated.formats.specdef.compounds.PtrList.PtrList)
		self.managers = Pointer(self.context, self.manager_count, generated.formats.specdef.compounds.PtrList.PtrList)
		self.scripts = Pointer(self.context, self.script_count, generated.formats.specdef.compounds.PtrList.PtrList)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.attrib_count = 0
		self.flags = 0
		self.name_count = 0
		self.childspec_count = 0
		self.manager_count = 0
		self.script_count = 0
		self.attribs = ArrayPointer(self.context, self.attrib_count, generated.formats.specdef.compounds.Spec.Spec)
		self.name_foreach_attribs = ForEachPointer(self.context, self.attribs, generated.formats.specdef.compounds.NamePtr.NamePtr)
		self.data_foreach_attribs = ForEachPointer(self.context, self.attribs, generated.formats.specdef.compounds.DataPtr.DataPtr)
		self.names = Pointer(self.context, self.name_count, generated.formats.specdef.compounds.PtrList.PtrList)
		self.childspecs = Pointer(self.context, self.childspec_count, generated.formats.specdef.compounds.PtrList.PtrList)
		self.managers = Pointer(self.context, self.manager_count, generated.formats.specdef.compounds.PtrList.PtrList)
		self.scripts = Pointer(self.context, self.script_count, generated.formats.specdef.compounds.PtrList.PtrList)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.attrib_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.flags = Ushort.from_stream(stream, instance.context, 0, None)
		instance.name_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.childspec_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.manager_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.script_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.attribs = ArrayPointer.from_stream(stream, instance.context, instance.attrib_count, generated.formats.specdef.compounds.Spec.Spec)
		instance.name_foreach_attribs = ForEachPointer.from_stream(stream, instance.context, instance.attribs, generated.formats.specdef.compounds.NamePtr.NamePtr)
		instance.data_foreach_attribs = ForEachPointer.from_stream(stream, instance.context, instance.attribs, generated.formats.specdef.compounds.DataPtr.DataPtr)
		instance.names = Pointer.from_stream(stream, instance.context, instance.name_count, generated.formats.specdef.compounds.PtrList.PtrList)
		instance.childspecs = Pointer.from_stream(stream, instance.context, instance.childspec_count, generated.formats.specdef.compounds.PtrList.PtrList)
		instance.managers = Pointer.from_stream(stream, instance.context, instance.manager_count, generated.formats.specdef.compounds.PtrList.PtrList)
		instance.scripts = Pointer.from_stream(stream, instance.context, instance.script_count, generated.formats.specdef.compounds.PtrList.PtrList)
		if not isinstance(instance.attribs, int):
			instance.attribs.arg = instance.attrib_count
		if not isinstance(instance.name_foreach_attribs, int):
			instance.name_foreach_attribs.arg = instance.attribs
		if not isinstance(instance.data_foreach_attribs, int):
			instance.data_foreach_attribs.arg = instance.attribs
		if not isinstance(instance.names, int):
			instance.names.arg = instance.name_count
		if not isinstance(instance.childspecs, int):
			instance.childspecs.arg = instance.childspec_count
		if not isinstance(instance.managers, int):
			instance.managers.arg = instance.manager_count
		if not isinstance(instance.scripts, int):
			instance.scripts.arg = instance.script_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ushort(instance.attrib_count)
		stream.write_ushort(instance.flags)
		stream.write_ubyte(instance.name_count)
		stream.write_ubyte(instance.childspec_count)
		stream.write_ubyte(instance.manager_count)
		stream.write_ubyte(instance.script_count)
		ArrayPointer.to_stream(stream, instance.attribs)
		ForEachPointer.to_stream(stream, instance.name_foreach_attribs)
		ForEachPointer.to_stream(stream, instance.data_foreach_attribs)
		Pointer.to_stream(stream, instance.names)
		Pointer.to_stream(stream, instance.childspecs)
		Pointer.to_stream(stream, instance.managers)
		Pointer.to_stream(stream, instance.scripts)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'attrib_count', Ushort, (0, None)
		yield 'flags', Ushort, (0, None)
		yield 'name_count', Ubyte, (0, None)
		yield 'childspec_count', Ubyte, (0, None)
		yield 'manager_count', Ubyte, (0, None)
		yield 'script_count', Ubyte, (0, None)
		yield 'attribs', ArrayPointer, (instance.attrib_count, generated.formats.specdef.compounds.Spec.Spec)
		yield 'name_foreach_attribs', ForEachPointer, (instance.attribs, generated.formats.specdef.compounds.NamePtr.NamePtr)
		yield 'data_foreach_attribs', ForEachPointer, (instance.attribs, generated.formats.specdef.compounds.DataPtr.DataPtr)
		yield 'names', Pointer, (instance.name_count, generated.formats.specdef.compounds.PtrList.PtrList)
		yield 'childspecs', Pointer, (instance.childspec_count, generated.formats.specdef.compounds.PtrList.PtrList)
		yield 'managers', Pointer, (instance.manager_count, generated.formats.specdef.compounds.PtrList.PtrList)
		yield 'scripts', Pointer, (instance.script_count, generated.formats.specdef.compounds.PtrList.PtrList)

	def get_info_str(self, indent=0):
		return f'SpecdefRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* attrib_count = {self.fmt_member(self.attrib_count, indent+1)}'
		s += f'\n	* flags = {self.fmt_member(self.flags, indent+1)}'
		s += f'\n	* name_count = {self.fmt_member(self.name_count, indent+1)}'
		s += f'\n	* childspec_count = {self.fmt_member(self.childspec_count, indent+1)}'
		s += f'\n	* manager_count = {self.fmt_member(self.manager_count, indent+1)}'
		s += f'\n	* script_count = {self.fmt_member(self.script_count, indent+1)}'
		s += f'\n	* attribs = {self.fmt_member(self.attribs, indent+1)}'
		s += f'\n	* name_foreach_attribs = {self.fmt_member(self.name_foreach_attribs, indent+1)}'
		s += f'\n	* data_foreach_attribs = {self.fmt_member(self.data_foreach_attribs, indent+1)}'
		s += f'\n	* names = {self.fmt_member(self.names, indent+1)}'
		s += f'\n	* childspecs = {self.fmt_member(self.childspecs, indent+1)}'
		s += f'\n	* managers = {self.fmt_member(self.managers, indent+1)}'
		s += f'\n	* scripts = {self.fmt_member(self.scripts, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
