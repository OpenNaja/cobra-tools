from generated.formats.compoundbrush.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class SomeStruct4Sub1(MemStruct):

	__name__ = 'SomeStruct4_SUB1'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.some_struct_4_sub_2_count = name_type_map['Uint64'](self.context, 0, None)
		self.some_struct_4_sub_1_string = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.some_struct_4_sub_2 = name_type_map['ArrayPointer'](self.context, self.some_struct_4_sub_2_count, name_type_map['SomeStruct4Sub2'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'some_struct_4_sub_1_string', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'some_struct_4_sub_2', name_type_map['ArrayPointer'], (None, name_type_map['SomeStruct4Sub2']), (False, None), (None, None)
		yield 'some_struct_4_sub_2_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'some_struct_4_sub_1_string', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'some_struct_4_sub_2', name_type_map['ArrayPointer'], (instance.some_struct_4_sub_2_count, name_type_map['SomeStruct4Sub2']), (False, None)
		yield 'some_struct_4_sub_2_count', name_type_map['Uint64'], (0, None), (False, None)
