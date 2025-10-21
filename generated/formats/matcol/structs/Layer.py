from generated.formats.matcol.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Layer(MemStruct):

	__name__ = 'Layer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_0 = name_type_map['Uint64'].from_value(0)
		self.zero_1 = name_type_map['Uint64'].from_value(0)
		self.float_attributes_count = name_type_map['Uint64'](self.context, 0, None)
		self.zero_2 = name_type_map['Uint64'].from_value(0)
		self.zero_3 = name_type_map['Uint64'].from_value(0)
		self.bool_attributes_count = name_type_map['Uint64'](self.context, 0, None)
		self.layer_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.float_attributes = name_type_map['ArrayPointer'](self.context, self.float_attributes_count, name_type_map['FloatAttrib'])
		self.bool_attributes = name_type_map['ArrayPointer'](self.context, self.bool_attributes_count, name_type_map['BoolAttrib'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'layer_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'zero_0', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'float_attributes', name_type_map['ArrayPointer'], (None, name_type_map['FloatAttrib']), (False, None), (None, None)
		yield 'float_attributes_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'zero_3', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'bool_attributes', name_type_map['ArrayPointer'], (None, name_type_map['BoolAttrib']), (False, None), (None, None)
		yield 'bool_attributes_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'layer_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'zero_0', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'float_attributes', name_type_map['ArrayPointer'], (instance.float_attributes_count, name_type_map['FloatAttrib']), (False, None)
		yield 'float_attributes_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'zero_3', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'bool_attributes', name_type_map['ArrayPointer'], (instance.bool_attributes_count, name_type_map['BoolAttrib']), (False, None)
		yield 'bool_attributes_count', name_type_map['Uint64'], (0, None), (False, None)
