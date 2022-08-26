from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.mechanicresearch.compounds.NextResearch import NextResearch
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Research(MemStruct):

	__name__ = 'Research'

	_import_path = 'generated.formats.mechanicresearch.compounds.Research'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0
		self.is_entry_level = 0
		self.unk_2 = 0
		self.next_research_count = 0
		self.unk_3 = 0
		self.unk_4 = 0
		self.item_name = Pointer(self.context, 0, ZString)
		self.next_research = Pointer(self.context, self.next_research_count, NextResearch)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_0 = 0
		self.is_entry_level = 0
		self.unk_2 = 0
		self.next_research_count = 0
		self.unk_3 = 0
		self.unk_4 = 0
		self.item_name = Pointer(self.context, 0, ZString)
		self.next_research = Pointer(self.context, self.next_research_count, NextResearch)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.item_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.unk_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.is_entry_level = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.next_research = Pointer.from_stream(stream, instance.context, instance.next_research_count, NextResearch)
		instance.next_research_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_3 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_4 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.item_name, int):
			instance.item_name.arg = 0
		if not isinstance(instance.next_research, int):
			instance.next_research.arg = instance.next_research_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.item_name)
		Uint.to_stream(stream, instance.unk_0)
		Uint.to_stream(stream, instance.is_entry_level)
		Uint64.to_stream(stream, instance.unk_2)
		Pointer.to_stream(stream, instance.next_research)
		Uint64.to_stream(stream, instance.next_research_count)
		Uint64.to_stream(stream, instance.unk_3)
		Uint64.to_stream(stream, instance.unk_4)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'item_name', Pointer, (0, ZString), (False, None)
		yield 'unk_0', Uint, (0, None), (False, None)
		yield 'is_entry_level', Uint, (0, None), (False, None)
		yield 'unk_2', Uint64, (0, None), (False, None)
		yield 'next_research', Pointer, (instance.next_research_count, NextResearch), (False, None)
		yield 'next_research_count', Uint64, (0, None), (False, None)
		yield 'unk_3', Uint64, (0, None), (False, None)
		yield 'unk_4', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Research [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* item_name = {self.fmt_member(self.item_name, indent+1)}'
		s += f'\n	* unk_0 = {self.fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* is_entry_level = {self.fmt_member(self.is_entry_level, indent+1)}'
		s += f'\n	* unk_2 = {self.fmt_member(self.unk_2, indent+1)}'
		s += f'\n	* next_research = {self.fmt_member(self.next_research, indent+1)}'
		s += f'\n	* next_research_count = {self.fmt_member(self.next_research_count, indent+1)}'
		s += f'\n	* unk_3 = {self.fmt_member(self.unk_3, indent+1)}'
		s += f'\n	* unk_4 = {self.fmt_member(self.unk_4, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
