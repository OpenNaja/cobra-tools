from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.researchdata.imports import name_type_map


class ResearchAffectedSquadloadout(MemStruct):

	__name__ = 'ResearchAffectedSquadloadout'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.affected_squad_loadout = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'affected_squad_loadout', name_type_map['Pointer'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'affected_squad_loadout', name_type_map['Pointer'], (0, None), (False, None)
