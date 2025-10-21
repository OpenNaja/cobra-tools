from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.techtree.imports import name_type_map


class TechLevel(MemStruct):

	__name__ = 'TechLevel'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.automatic_research_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_0 = name_type_map['Int'](self.context, 0, None)
		self.unlockable_research_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_1 = name_type_map['Int'](self.context, 0, None)
		self.mutexed_unlockable_research_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_2 = name_type_map['Int'](self.context, 0, None)
		self.automatic_research = name_type_map['ArrayPointer'](self.context, self.automatic_research_count, name_type_map['ResearchDataDep'])
		self.unlockable_research = name_type_map['ArrayPointer'](self.context, self.unlockable_research_count, name_type_map['ResearchDataDep'])
		self.mutexed_unlockable_research = name_type_map['ArrayPointer'](self.context, self.mutexed_unlockable_research_count, name_type_map['MutexResearch'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'automatic_research', name_type_map['ArrayPointer'], (None, name_type_map['ResearchDataDep']), (False, None), (None, None)
		yield 'automatic_research_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_0', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'unlockable_research', name_type_map['ArrayPointer'], (None, name_type_map['ResearchDataDep']), (False, None), (None, None)
		yield 'unlockable_research_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_1', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'mutexed_unlockable_research', name_type_map['ArrayPointer'], (None, name_type_map['MutexResearch']), (False, None), (None, None)
		yield 'mutexed_unlockable_research_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_2', name_type_map['Int'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'automatic_research', name_type_map['ArrayPointer'], (instance.automatic_research_count, name_type_map['ResearchDataDep']), (False, None)
		yield 'automatic_research_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_0', name_type_map['Int'], (0, None), (False, None)
		yield 'unlockable_research', name_type_map['ArrayPointer'], (instance.unlockable_research_count, name_type_map['ResearchDataDep']), (False, None)
		yield 'unlockable_research_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_1', name_type_map['Int'], (0, None), (False, None)
		yield 'mutexed_unlockable_research', name_type_map['ArrayPointer'], (instance.mutexed_unlockable_research_count, name_type_map['MutexResearch']), (False, None)
		yield 'mutexed_unlockable_research_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_2', name_type_map['Int'], (0, None), (False, None)
