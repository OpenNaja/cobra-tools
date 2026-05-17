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
		self.a = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.c = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', Array, (0, None, (15,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'floats', Array, (0, None, (4, 3,), name_type_map['Float']), (False, None), (None, None)
		yield 'c', Array, (0, None, (14,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Array, (0, None, (15,), name_type_map['Uint64']), (False, None)
		yield 'floats', Array, (0, None, (4, 3,), name_type_map['Float']), (False, None)
		yield 'c', Array, (0, None, (14,), name_type_map['Uint']), (False, None)
