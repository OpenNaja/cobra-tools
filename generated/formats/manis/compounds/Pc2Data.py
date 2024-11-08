from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class Pc2Data(BaseStruct):

	"""
	in seemingly uncompressed manis
	"""

	__name__ = 'PC2Data'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.a = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.pad = name_type_map['PadAlign'](self.context, 16, self.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'a', Array, (0, None, (144,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'pad', name_type_map['PadAlign'], (16, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'a', Array, (0, None, (144,), name_type_map['Ubyte']), (False, None)
		yield 'pad', name_type_map['PadAlign'], (16, instance.ref), (False, None)
