from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class UshortLut(BaseStruct):

	"""
	found in WH
	in seemingly uncompressed manis
	"""

	__name__ = 'UshortLut'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.align = name_type_map['SmartPadding'](self.context, 0, None)
		self.a = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.b = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.zeros = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.target_bone_count = name_type_map['Uint'](self.context, 0, None)
		self.offsets = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.flags = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.ref_2 = name_type_map['Empty'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'align', name_type_map['SmartPadding'], (0, None), (False, None), (None, None)
		yield 'a', Array, (0, None, (48,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'b', Array, (0, None, (48,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'zeros', Array, (0, None, (48,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'target_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'offsets', Array, (0, None, (82,), name_type_map['Uint']), (False, None), (None, None)
		yield 'flags', Array, (0, None, (96,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'align', name_type_map['SmartPadding'], (0, None), (False, None)
		yield 'a', Array, (0, None, (48,), name_type_map['Ubyte']), (False, None)
		yield 'b', Array, (0, None, (48,), name_type_map['Ubyte']), (False, None)
		yield 'zeros', Array, (0, None, (48,), name_type_map['Ubyte']), (False, None)
		yield 'target_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'offsets', Array, (0, None, (82,), name_type_map['Uint']), (False, None)
		yield 'flags', Array, (0, None, (96,), name_type_map['Ubyte']), (False, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None)
