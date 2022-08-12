from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.mechanicresearch.compound.NextResearch
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class Research(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.unk_0 = 0
		self.is_entry_level = 0
		self.unk_2 = 0
		self.next_research_count = 0
		self.unk_3 = 0
		self.unk_4 = 0
		self.item_name = 0
		self.next_research = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk_0 = 0
		self.is_entry_level = 0
		self.unk_2 = 0
		self.next_research_count = 0
		self.unk_3 = 0
		self.unk_4 = 0
		self.item_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.next_research = Pointer(self.context, self.next_research_count, generated.formats.mechanicresearch.compound.NextResearch.NextResearch)

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
		instance.item_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.unk_0 = stream.read_uint()
		instance.is_entry_level = stream.read_uint()
		instance.unk_2 = stream.read_uint64()
		instance.next_research = Pointer.from_stream(stream, instance.context, instance.next_research_count, generated.formats.mechanicresearch.compound.NextResearch.NextResearch)
		instance.next_research_count = stream.read_uint64()
		instance.unk_3 = stream.read_uint64()
		instance.unk_4 = stream.read_uint64()
		instance.item_name.arg = 0
		instance.next_research.arg = instance.next_research_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.item_name)
		stream.write_uint(instance.unk_0)
		stream.write_uint(instance.is_entry_level)
		stream.write_uint64(instance.unk_2)
		Pointer.to_stream(stream, instance.next_research)
		stream.write_uint64(instance.next_research_count)
		stream.write_uint64(instance.unk_3)
		stream.write_uint64(instance.unk_4)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('item_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('unk_0', Uint, (0, None))
		yield ('is_entry_level', Uint, (0, None))
		yield ('unk_2', Uint64, (0, None))
		yield ('next_research', Pointer, (instance.next_research_count, generated.formats.mechanicresearch.compound.NextResearch.NextResearch))
		yield ('next_research_count', Uint64, (0, None))
		yield ('unk_3', Uint64, (0, None))
		yield ('unk_4', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'Research [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* item_name = {fmt_member(self.item_name, indent+1)}'
		s += f'\n	* unk_0 = {fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* is_entry_level = {fmt_member(self.is_entry_level, indent+1)}'
		s += f'\n	* unk_2 = {fmt_member(self.unk_2, indent+1)}'
		s += f'\n	* next_research = {fmt_member(self.next_research, indent+1)}'
		s += f'\n	* next_research_count = {fmt_member(self.next_research_count, indent+1)}'
		s += f'\n	* unk_3 = {fmt_member(self.unk_3, indent+1)}'
		s += f'\n	* unk_4 = {fmt_member(self.unk_4, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
