from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class CompressedManiDataPC2(BaseStruct):

	"""
	in compressed manis
	"""

	__name__ = 'CompressedManiDataPC2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.size = name_type_map['Uint'](self.context, 0, None)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.databytes = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.ref_2 = name_type_map['Empty'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'databytes', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'size', name_type_map['Uint'], (0, None), (False, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'databytes', Array, (0, None, (instance.size - 4,), name_type_map['Ubyte']), (False, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None)
