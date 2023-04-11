from generated.formats.animalresearch.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ResearchLevel(MemStruct):

	__name__ = 'ResearchLevel'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.next_level_count = name_type_map['Uint64'](self.context, 0, None)
		self.children_count = name_type_map['Uint64'](self.context, 0, None)
		self.level_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.next_levels = name_type_map['Pointer'](self.context, self.next_level_count, name_type_map['PtrList'])
		self.children = name_type_map['Pointer'](self.context, self.children_count, name_type_map['PtrList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'level_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'next_levels', name_type_map['Pointer'], (None, name_type_map['PtrList']), (False, None), (None, None)
		yield 'next_level_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'children', name_type_map['Pointer'], (None, name_type_map['PtrList']), (False, None), (None, None)
		yield 'children_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'level_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'next_levels', name_type_map['Pointer'], (instance.next_level_count, name_type_map['PtrList']), (False, None)
		yield 'next_level_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'children', name_type_map['Pointer'], (instance.children_count, name_type_map['PtrList']), (False, None)
		yield 'children_count', name_type_map['Uint64'], (0, None), (False, None)
