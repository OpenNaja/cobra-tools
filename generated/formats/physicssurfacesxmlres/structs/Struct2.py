from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class Struct2(MemStruct):

	"""
	PC: 24 bytes
	"""

	__name__ = 'Struct2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = name_type_map['Ushort'](self.context, 0, None)
		self.short_2 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_32_2 = name_type_map['Uint'](self.context, 0, None)
		self.name_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.arr = name_type_map['ArrayPointer'](self.context, self.count, name_type_map['Struct2Sub'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'arr', name_type_map['ArrayPointer'], (None, name_type_map['Struct2Sub']), (False, None), (None, None)
		yield 'count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'short_2', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_32_2', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'arr', name_type_map['ArrayPointer'], (instance.count, name_type_map['Struct2Sub']), (False, None)
		yield 'count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'short_2', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_32_2', name_type_map['Uint'], (0, None), (False, None)
