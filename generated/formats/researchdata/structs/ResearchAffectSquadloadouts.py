from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.researchdata.imports import name_type_map


class ResearchAffectSquadloadouts(MemStruct):

	__name__ = 'ResearchAffectSquadloadouts'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.affected_squadloadout_count = name_type_map['Uint64'](self.context, 0, None)
		self.research_loc = name_type_map['ArrayPointer'](self.context, self.affected_squadloadout_count, name_type_map['ResearchAffectedSquadloadout'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'research_loc', name_type_map['ArrayPointer'], (None, name_type_map['ResearchAffectedSquadloadout']), (False, None), (None, None)
		yield 'affected_squadloadout_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'research_loc', name_type_map['ArrayPointer'], (instance.affected_squadloadout_count, name_type_map['ResearchAffectedSquadloadout']), (False, None)
		yield 'affected_squadloadout_count', name_type_map['Uint64'], (0, None), (False, None)
