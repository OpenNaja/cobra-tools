from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.techtree.imports import name_type_map


class TechTreeRoot(MemStruct):

	__name__ = 'TechTreeRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.buffer_0 = name_type_map['Int'](self.context, 0, None)
		self.buffer_1 = name_type_map['Int'](self.context, 0, None)
		self.tech_levels_count = name_type_map['Uint64'](self.context, 0, None)
		self.filename = name_type_map['Pointer'](self.context, 0, name_type_map['ZStringObfuscated'])
		self.tech_levels = name_type_map['ArrayPointer'](self.context, self.tech_levels_count, name_type_map['TechLevel'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'filename', name_type_map['Pointer'], (0, name_type_map['ZStringObfuscated']), (False, None), (None, None)
		yield 'buffer_0', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'buffer_1', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'tech_levels', name_type_map['ArrayPointer'], (None, name_type_map['TechLevel']), (False, None), (None, None)
		yield 'tech_levels_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'filename', name_type_map['Pointer'], (0, name_type_map['ZStringObfuscated']), (False, None)
		yield 'buffer_0', name_type_map['Int'], (0, None), (False, None)
		yield 'buffer_1', name_type_map['Int'], (0, None), (False, None)
		yield 'tech_levels', name_type_map['ArrayPointer'], (instance.tech_levels_count, name_type_map['TechLevel']), (False, None)
		yield 'tech_levels_count', name_type_map['Uint64'], (0, None), (False, None)
