from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.researchdata.imports import name_type_map


class ResearchDataAppliesToSquad(MemStruct):

	__name__ = 'ResearchDataAppliesToSquad'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dependency_name = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'dependency_name', name_type_map['Pointer'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'dependency_name', name_type_map['Pointer'], (0, None), (False, None)
