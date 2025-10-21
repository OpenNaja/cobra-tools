from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.techtree.imports import name_type_map


class ResearchDataDep(MemStruct):

	__name__ = 'ResearchDataDep'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.research_data_dependency = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'research_data_dependency', name_type_map['Pointer'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'research_data_dependency', name_type_map['Pointer'], (0, None), (False, None)
