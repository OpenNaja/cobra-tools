from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class Repeat(BaseStruct):

	__name__ = 'Repeat'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros_0 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])

		# to be read sequentially starting after this array
		self.byte_size = name_type_map['Uint64'](self.context, 0, None)
		self.zeros_1 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'zeros_0', Array, (0, None, (7,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'byte_size', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zeros_1', Array, (0, None, (2,), name_type_map['Uint64']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zeros_0', Array, (0, None, (7,), name_type_map['Uint64']), (False, None)
		yield 'byte_size', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zeros_1', Array, (0, None, (2,), name_type_map['Uint64']), (False, None)
