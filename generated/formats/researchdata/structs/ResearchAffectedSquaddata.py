from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.researchdata.imports import name_type_map


class ResearchAffectedSquaddata(MemStruct):

	__name__ = 'ResearchAffectedSquaddata'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.affected_squaddata_from = name_type_map['Pointer'](self.context, 0, None)
		self.affected_squaddata_to = name_type_map['Pointer'](self.context, 0, None)
		self.affected_squad_transition_fx = name_type_map['Pointer'](self.context, 0, name_type_map['ResearchFXData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'affected_squaddata_from', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'affected_squaddata_to', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'affected_squad_transition_fx', name_type_map['Pointer'], (0, name_type_map['ResearchFXData']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'affected_squaddata_from', name_type_map['Pointer'], (0, None), (False, None)
		yield 'affected_squaddata_to', name_type_map['Pointer'], (0, None), (False, None)
		yield 'affected_squad_transition_fx', name_type_map['Pointer'], (0, name_type_map['ResearchFXData']), (False, None)
