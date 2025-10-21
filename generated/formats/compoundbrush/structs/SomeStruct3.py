from generated.array import Array
from generated.formats.compoundbrush.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class SomeStruct3(MemStruct):

	__name__ = 'SomeStruct3'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unknown_int_1 = name_type_map['Uint'](self.context, 0, None)
		self.some_struct_3_sub_1_count = name_type_map['Uint64'](self.context, 0, None)
		self.unknown_ints = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.brush_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_struct_1 = name_type_map['ArrayPointer'](self.context, self.some_struct_3_sub_1_count, name_type_map['SomeStruct3Sub1'])
		self.unknown_struct_2 = name_type_map['ArrayPointer'](self.context, self.some_struct_3_sub_1_count, name_type_map['SomeStruct3Sub1'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'brush_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_struct_1', name_type_map['ArrayPointer'], (None, name_type_map['SomeStruct3Sub1']), (False, None), (None, None)
		yield 'unknown_struct_2', name_type_map['ArrayPointer'], (None, name_type_map['SomeStruct3Sub1']), (False, None), (None, None)
		yield 'unknown_int_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'some_struct_3_sub_1_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unknown_ints', Array, (0, None, (11,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'brush_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_struct_1', name_type_map['ArrayPointer'], (instance.some_struct_3_sub_1_count, name_type_map['SomeStruct3Sub1']), (False, None)
		yield 'unknown_struct_2', name_type_map['ArrayPointer'], (instance.some_struct_3_sub_1_count, name_type_map['SomeStruct3Sub1']), (False, None)
		yield 'unknown_int_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'some_struct_3_sub_1_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unknown_ints', Array, (0, None, (11,), name_type_map['Uint']), (False, None)
