from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class StructA(BaseStruct):

	"""
	PC2: 16 bytes
	"""

	__name__ = 'StructA'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = Array(self.context, 0, None, (0,), name_type_map['Byte'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data', Array, (0, None, (16,), name_type_map['Byte']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data', Array, (0, None, (16,), name_type_map['Byte']), (False, None)
