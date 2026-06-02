from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class Struct2(BaseStruct):

	"""
	224 bytes
	"""

	__name__ = 'Struct2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = name_type_map['Uint'](self.context, 0, None)
		self.b = name_type_map['Int'](self.context, 0, None)
		self.z = name_type_map['Int'](self.context, 0, None)
		self.c = name_type_map['Short'](self.context, 0, None)
		self.d = name_type_map['Short'](self.context, 0, None)
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.e = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.floats_2 = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.f = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.floats_3 = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.g = name_type_map['Uint'](self.context, 0, None)
		self.h = name_type_map['Ushort'](self.context, 0, None)
		self.i = name_type_map['Ubyte'](self.context, 0, None)
		self.j = name_type_map['Ubyte'](self.context, 0, None)
		self.zfinal = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'z', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'c', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'd', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'floats', Array, (0, None, (3, 4,), name_type_map['Float']), (False, None), (None, None)
		yield 'e', Array, (0, None, (4,), name_type_map['Uint']), (False, None), (None, None)
		yield 'floats_2', Array, (0, None, (6,), name_type_map['Float']), (False, None), (None, None)
		yield 'f', Array, (0, None, (4,), name_type_map['Uint']), (False, None), (None, None)
		yield 'floats_3', Array, (0, None, (6,), name_type_map['Float']), (False, None), (None, None)
		yield 'g', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'h', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'i', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'j', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'zfinal', Array, (0, None, (9,), name_type_map['Uint64']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', name_type_map['Uint'], (0, None), (False, None)
		yield 'b', name_type_map['Int'], (0, None), (False, None)
		yield 'z', name_type_map['Int'], (0, None), (False, None)
		yield 'c', name_type_map['Short'], (0, None), (False, None)
		yield 'd', name_type_map['Short'], (0, None), (False, None)
		yield 'floats', Array, (0, None, (3, 4,), name_type_map['Float']), (False, None)
		yield 'e', Array, (0, None, (4,), name_type_map['Uint']), (False, None)
		yield 'floats_2', Array, (0, None, (6,), name_type_map['Float']), (False, None)
		yield 'f', Array, (0, None, (4,), name_type_map['Uint']), (False, None)
		yield 'floats_3', Array, (0, None, (6,), name_type_map['Float']), (False, None)
		yield 'g', name_type_map['Uint'], (0, None), (False, None)
		yield 'h', name_type_map['Ushort'], (0, None), (False, None)
		yield 'i', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'j', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'zfinal', Array, (0, None, (9,), name_type_map['Uint64']), (False, None)
