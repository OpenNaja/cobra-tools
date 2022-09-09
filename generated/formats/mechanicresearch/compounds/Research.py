from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
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
		self.next_research = Pointer(self.context, self.next_research_count, Research._import_path_map["generated.formats.mechanicresearch.compounds.NextResearch"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item_name', Pointer, (0, ZString), (False, None)
		yield 'unk_0', Uint, (0, None), (False, None)
		yield 'is_entry_level', Uint, (0, None), (False, None)
		yield 'unk_2', Uint64, (0, None), (False, None)
		yield 'next_research', Pointer, (instance.next_research_count, Research._import_path_map["generated.formats.mechanicresearch.compounds.NextResearch"]), (False, None)
		yield 'next_research_count', Uint64, (0, None), (False, None)
		yield 'unk_3', Uint64, (0, None), (False, None)
		yield 'unk_4', Uint64, (0, None), (False, None)
