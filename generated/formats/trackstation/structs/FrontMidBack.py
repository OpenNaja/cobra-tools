from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class FrontMidBack(MemStruct):

	__name__ = 'FrontMidBack'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.front_rotation = name_type_map['Ubyte'](self.context, 0, None)
		self.middle_rotation = name_type_map['Ubyte'](self.context, 0, None)
		self.back_rotation = name_type_map['Ubyte'](self.context, 0, None)
		self.unkown_byte_0 = name_type_map['Ubyte'].from_value(0)
		self.unkown_byte_1 = name_type_map['Ubyte'].from_value(0)
		self.unkown_byte_2 = name_type_map['Ubyte'].from_value(0)
		self.unkown_byte_3 = name_type_map['Ubyte'].from_value(0)
		self.unkown_byte_4 = name_type_map['Ubyte'].from_value(0)
		self.front = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.middle = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.back = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'front', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'middle', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'back', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'front_rotation', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'middle_rotation', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'back_rotation', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'unkown_byte_0', name_type_map['Ubyte'], (0, None), (True, 0), (None, None)
		yield 'unkown_byte_1', name_type_map['Ubyte'], (0, None), (True, 0), (None, None)
		yield 'unkown_byte_2', name_type_map['Ubyte'], (0, None), (True, 0), (None, None)
		yield 'unkown_byte_3', name_type_map['Ubyte'], (0, None), (True, 0), (None, None)
		yield 'unkown_byte_4', name_type_map['Ubyte'], (0, None), (True, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'front', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'middle', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'back', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'front_rotation', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'middle_rotation', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'back_rotation', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'unkown_byte_0', name_type_map['Ubyte'], (0, None), (True, 0)
		yield 'unkown_byte_1', name_type_map['Ubyte'], (0, None), (True, 0)
		yield 'unkown_byte_2', name_type_map['Ubyte'], (0, None), (True, 0)
		yield 'unkown_byte_3', name_type_map['Ubyte'], (0, None), (True, 0)
		yield 'unkown_byte_4', name_type_map['Ubyte'], (0, None), (True, 0)
