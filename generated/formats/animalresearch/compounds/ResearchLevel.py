from generated.formats.animalresearch.compounds.PtrList import PtrList
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ResearchLevel(MemStruct):

	__name__ = 'ResearchLevel'

	_import_path = 'generated.formats.animalresearch.compounds.ResearchLevel'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.next_level_count = 0
		self.children_count = 0
		self.level_name = Pointer(self.context, 0, ZString)
		self.next_levels = Pointer(self.context, self.next_level_count, PtrList)
		self.children = Pointer(self.context, self.children_count, PtrList)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.next_level_count = 0
		self.children_count = 0
		self.level_name = Pointer(self.context, 0, ZString)
		self.next_levels = Pointer(self.context, self.next_level_count, PtrList)
		self.children = Pointer(self.context, self.children_count, PtrList)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.level_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.next_levels = Pointer.from_stream(stream, instance.context, instance.next_level_count, PtrList)
		instance.next_level_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.children = Pointer.from_stream(stream, instance.context, instance.children_count, PtrList)
		instance.children_count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.level_name, int):
			instance.level_name.arg = 0
		if not isinstance(instance.next_levels, int):
			instance.next_levels.arg = instance.next_level_count
		if not isinstance(instance.children, int):
			instance.children.arg = instance.children_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.level_name)
		Pointer.to_stream(stream, instance.next_levels)
		Uint64.to_stream(stream, instance.next_level_count)
		Pointer.to_stream(stream, instance.children)
		Uint64.to_stream(stream, instance.children_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'level_name', Pointer, (0, ZString), (False, None)
		yield 'next_levels', Pointer, (instance.next_level_count, PtrList), (False, None)
		yield 'next_level_count', Uint64, (0, None), (False, None)
		yield 'children', Pointer, (instance.children_count, PtrList), (False, None)
		yield 'children_count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ResearchLevel [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* level_name = {self.fmt_member(self.level_name, indent+1)}'
		s += f'\n	* next_levels = {self.fmt_member(self.next_levels, indent+1)}'
		s += f'\n	* next_level_count = {self.fmt_member(self.next_level_count, indent+1)}'
		s += f'\n	* children = {self.fmt_member(self.children, indent+1)}'
		s += f'\n	* children_count = {self.fmt_member(self.children_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
