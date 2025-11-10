from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class CompressedHeader(BaseStruct):

	"""
	present at end of buffer 0 in JWE3 if any of the manis is compressed
	"""

	__name__ = 'CompressedHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.size = name_type_map['Uint'](self.context, 0, None)
		self.u_0 = name_type_map['Ubyte'](self.context, 0, None)
		self.u_1 = name_type_map['Ubyte'](self.context, 0, None)
		self.u_2 = name_type_map['Ubyte'](self.context, 0, None)
		self.u_3 = name_type_map['Ubyte'](self.context, 0, None)
		self.const_0 = name_type_map['Ubyte'].from_value(1)
		self.const_1 = name_type_map['Ubyte'].from_value(219)
		self.const_2 = name_type_map['Ubyte'].from_value(17)
		self.const_3 = name_type_map['Ubyte'].from_value(172)
		self.a = name_type_map['Uint'].from_value(10)
		self.b = name_type_map['Uint'].from_value(1)

		# or 2
		self.unk_count = name_type_map['Uint'].from_value(1)
		self.d = name_type_map['Ushort'].from_value(0)
		self.e = name_type_map['Ushort'].from_value(16)
		self.mani_count = name_type_map['Uint'](self.context, 0, None)
		self.g = name_type_map['Uint'](self.context, 0, None)
		self.h = name_type_map['Uint'](self.context, 0, None)
		self.unka = name_type_map['Uint'](self.context, 0, None)
		self.unkb = name_type_map['Uint'](self.context, 0, None)
		self.minus_1 = name_type_map['Int64'].from_value(-1)
		self.x = name_type_map['Int64'](self.context, 0, None)
		self.y = name_type_map['Int64'](self.context, 0, None)
		self.pointers_1 = Array(self.context, 0, None, (0,), name_type_map['CompressedPointer'])
		self.pointers_2 = Array(self.context, 0, None, (0,), name_type_map['CompressedPointer'])
		self.pad = name_type_map['PadAlign'](self.context, 16, self.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'u_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'u_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'u_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'u_3', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'const_0', name_type_map['Ubyte'], (0, None), (False, 1), (None, None)
		yield 'const_1', name_type_map['Ubyte'], (0, None), (False, 219), (None, None)
		yield 'const_2', name_type_map['Ubyte'], (0, None), (False, 17), (None, None)
		yield 'const_3', name_type_map['Ubyte'], (0, None), (False, 172), (None, None)
		yield 'a', name_type_map['Uint'], (0, None), (False, 10), (None, None)
		yield 'b', name_type_map['Uint'], (0, None), (False, 1), (None, None)
		yield 'unk_count', name_type_map['Uint'], (0, None), (False, 1), (None, None)
		yield 'd', name_type_map['Ushort'], (0, None), (False, 0), (None, None)
		yield 'e', name_type_map['Ushort'], (0, None), (False, 16), (None, None)
		yield 'mani_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'g', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'h', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unka', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unkb', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'minus_1', name_type_map['Int64'], (0, None), (False, -1), (None, None)
		yield 'x', name_type_map['Int64'], (0, None), (False, None), (None, None)
		yield 'y', name_type_map['Int64'], (0, None), (False, None), (None, None)
		yield 'pointers_1', Array, (0, None, (None,), name_type_map['CompressedPointer']), (False, None), (None, None)
		yield 'pointers_2', Array, (0, None, (None,), name_type_map['CompressedPointer']), (False, None), (None, None)
		yield 'pad', name_type_map['PadAlign'], (16, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'size', name_type_map['Uint'], (0, None), (False, None)
		yield 'u_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'u_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'u_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'u_3', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'const_0', name_type_map['Ubyte'], (0, None), (False, 1)
		yield 'const_1', name_type_map['Ubyte'], (0, None), (False, 219)
		yield 'const_2', name_type_map['Ubyte'], (0, None), (False, 17)
		yield 'const_3', name_type_map['Ubyte'], (0, None), (False, 172)
		yield 'a', name_type_map['Uint'], (0, None), (False, 10)
		yield 'b', name_type_map['Uint'], (0, None), (False, 1)
		yield 'unk_count', name_type_map['Uint'], (0, None), (False, 1)
		yield 'd', name_type_map['Ushort'], (0, None), (False, 0)
		yield 'e', name_type_map['Ushort'], (0, None), (False, 16)
		yield 'mani_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'g', name_type_map['Uint'], (0, None), (False, None)
		yield 'h', name_type_map['Uint'], (0, None), (False, None)
		yield 'unka', name_type_map['Uint'], (0, None), (False, None)
		yield 'unkb', name_type_map['Uint'], (0, None), (False, None)
		yield 'minus_1', name_type_map['Int64'], (0, None), (False, -1)
		yield 'x', name_type_map['Int64'], (0, None), (False, None)
		yield 'y', name_type_map['Int64'], (0, None), (False, None)
		yield 'pointers_1', Array, (0, None, (instance.unk_count,), name_type_map['CompressedPointer']), (False, None)
		yield 'pointers_2', Array, (0, None, (instance.mani_count,), name_type_map['CompressedPointer']), (False, None)
		yield 'pad', name_type_map['PadAlign'], (16, instance.ref), (False, None)
