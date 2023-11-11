from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class ElemZt(BaseStruct):

	__name__ = 'ElemZt'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.a = name_type_map['Ushort'](self.context, 0, None)
		self.b = name_type_map['Ushort'](self.context, 0, None)
		self.c = name_type_map['Ushort'](self.context, 0, None)
		self.d = name_type_map['Ushort'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None), (None, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'c', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'd', name_type_map['Ushort'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None)
		yield 'c', name_type_map['Ushort'], (0, None), (False, None)
		yield 'd', name_type_map['Ushort'], (0, None), (False, None)
