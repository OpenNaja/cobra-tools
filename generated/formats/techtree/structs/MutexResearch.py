from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.techtree.imports import name_type_map


class MutexResearch(MemStruct):

	__name__ = 'MutexResearch'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mutex_options_count = name_type_map['Uint64'](self.context, 0, None)
		self.mutex_options = name_type_map['ArrayPointer'](self.context, self.mutex_options_count, name_type_map['ResearchDataDep'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'mutex_options', name_type_map['ArrayPointer'], (None, name_type_map['ResearchDataDep']), (False, None), (None, None)
		yield 'mutex_options_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'mutex_options', name_type_map['ArrayPointer'], (instance.mutex_options_count, name_type_map['ResearchDataDep']), (False, None)
		yield 'mutex_options_count', name_type_map['Uint64'], (0, None), (False, None)
