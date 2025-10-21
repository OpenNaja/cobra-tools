from generated.formats.animalresearch.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ResearchRoot(MemStruct):

	__name__ = 'ResearchRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.levels_count = name_type_map['Uint64'](self.context, 0, None)
		self.levels = name_type_map['ArrayPointer'](self.context, self.levels_count, name_type_map['ResearchLevel'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'levels', name_type_map['ArrayPointer'], (None, name_type_map['ResearchLevel']), (False, None), (None, None)
		yield 'levels_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'levels', name_type_map['ArrayPointer'], (instance.levels_count, name_type_map['ResearchLevel']), (False, None)
		yield 'levels_count', name_type_map['Uint64'], (0, None), (False, None)
