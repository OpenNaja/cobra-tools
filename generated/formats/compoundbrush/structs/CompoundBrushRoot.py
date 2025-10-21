from generated.formats.compoundbrush.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CompoundBrushRoot(MemStruct):

	__name__ = 'CompoundBrushRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.brushes_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_2_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_3_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_4_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_5_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_6_count = name_type_map['Uint'](self.context, 0, None)
		self.unknown_7_count = name_type_map['Uint'](self.context, 0, None)
		self.brushes = name_type_map['ArrayPointer'](self.context, self.brushes_count, name_type_map['BrushStruct'])
		self.pointer_2 = name_type_map['Pointer'](self.context, self.unknown_2_count, name_type_map['ZStringList'])
		self.pointer_3 = name_type_map['ArrayPointer'](self.context, self.unknown_3_count, name_type_map['SomeStruct3'])
		self.pointer_4 = name_type_map['ArrayPointer'](self.context, self.unknown_4_count, name_type_map['SomeStruct4'])
		self.pointer_5 = name_type_map['Pointer'](self.context, self.unknown_7_count, name_type_map['ZStringList'])
		self.pointer_6 = name_type_map['Pointer'](self.context, self.unknown_7_count, name_type_map['ZStringList'])
		self.pointer_7 = name_type_map['ArrayPointer'](self.context, 3, name_type_map['SomeStruct4Sub2'])
		self.pointer_8 = name_type_map['Pointer'](self.context, 0, name_type_map['SomeStruct8'])
		self.mask_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'brushes', name_type_map['ArrayPointer'], (None, name_type_map['BrushStruct']), (False, None), (None, None)
		yield 'pointer_2', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'pointer_3', name_type_map['ArrayPointer'], (None, name_type_map['SomeStruct3']), (False, None), (None, None)
		yield 'pointer_4', name_type_map['ArrayPointer'], (None, name_type_map['SomeStruct4']), (False, None), (None, None)
		yield 'pointer_5', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'pointer_6', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'pointer_7', name_type_map['ArrayPointer'], (3, name_type_map['SomeStruct4Sub2']), (False, None), (None, None)
		yield 'pointer_8', name_type_map['Pointer'], (0, name_type_map['SomeStruct8']), (False, None), (None, None)
		yield 'mask_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'brushes_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_2_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_3_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_4_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_5_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_6_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_7_count', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'brushes', name_type_map['ArrayPointer'], (instance.brushes_count, name_type_map['BrushStruct']), (False, None)
		yield 'pointer_2', name_type_map['Pointer'], (instance.unknown_2_count, name_type_map['ZStringList']), (False, None)
		yield 'pointer_3', name_type_map['ArrayPointer'], (instance.unknown_3_count, name_type_map['SomeStruct3']), (False, None)
		yield 'pointer_4', name_type_map['ArrayPointer'], (instance.unknown_4_count, name_type_map['SomeStruct4']), (False, None)
		yield 'pointer_5', name_type_map['Pointer'], (instance.unknown_7_count, name_type_map['ZStringList']), (False, None)
		yield 'pointer_6', name_type_map['Pointer'], (instance.unknown_7_count, name_type_map['ZStringList']), (False, None)
		yield 'pointer_7', name_type_map['ArrayPointer'], (3, name_type_map['SomeStruct4Sub2']), (False, None)
		yield 'pointer_8', name_type_map['Pointer'], (0, name_type_map['SomeStruct8']), (False, None)
		yield 'mask_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'brushes_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_2_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_3_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_4_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_5_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_6_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_7_count', name_type_map['Uint'], (0, None), (False, None)
