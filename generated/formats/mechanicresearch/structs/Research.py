from generated.formats.mechanicresearch.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Research(MemStruct):

	__name__ = 'Research'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Set to 1 for researchs completed (e.g. scenario level2  will have level1 unlocked already)
		self.is_completed = name_type_map['Uint'](self.context, 0, None)

		# First research enabled level (0 if research is complete)
		self.is_entry_level = name_type_map['Uint'](self.context, 0, None)

		# At least one research item needs to have 1 to enable research on this tree (all 0 used for noneresearchable)
		self.is_enabled = name_type_map['Uint64'](self.context, 0, None)
		self.next_research_count = name_type_map['Uint64'](self.context, 0, None)
		self.unk_3 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_4 = name_type_map['Uint64'](self.context, 0, None)
		self.item_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.next_research = name_type_map['Pointer'](self.context, self.next_research_count, name_type_map['NextResearch'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'item_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'is_completed', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'is_entry_level', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'is_enabled', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'next_research', name_type_map['Pointer'], (None, name_type_map['NextResearch']), (False, None), (None, None)
		yield 'next_research_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_4', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'is_completed', name_type_map['Uint'], (0, None), (False, None)
		yield 'is_entry_level', name_type_map['Uint'], (0, None), (False, None)
		yield 'is_enabled', name_type_map['Uint64'], (0, None), (False, None)
		yield 'next_research', name_type_map['Pointer'], (instance.next_research_count, name_type_map['NextResearch']), (False, None)
		yield 'next_research_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_4', name_type_map['Uint64'], (0, None), (False, None)
