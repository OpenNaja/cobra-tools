from generated.formats.compoundbrush.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class SomeStruct4Sub2(MemStruct):

	__name__ = 'SomeStruct4_SUB2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unknown_1_int = name_type_map['Uint'](self.context, 0, None)
		self.unknown_1_float = name_type_map['Float'](self.context, 0, None)
		self.unknown_2_float = name_type_map['Float'](self.context, 0, None)
		self.unknown_3_float = name_type_map['Float'](self.context, 0, None)
		self.some_struct_4_sub_2_string = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'some_struct_4_sub_2_string', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_1_int', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_1_float', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unknown_2_float', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unknown_3_float', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'some_struct_4_sub_2_string', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_1_int', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_1_float', name_type_map['Float'], (0, None), (False, None)
		yield 'unknown_2_float', name_type_map['Float'], (0, None), (False, None)
		yield 'unknown_3_float', name_type_map['Float'], (0, None), (False, None)
