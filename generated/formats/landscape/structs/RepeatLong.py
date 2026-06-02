from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class RepeatLong(BaseStruct):

	"""
	16 bytes
	"""

	__name__ = 'RepeatLong'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero = name_type_map['Uint64'](self.context, 0, None)
		self.ind = name_type_map['Ushort'](self.context, 0, None)
		self.pair = Array(self.context, 0, None, (0,), name_type_map['Pair'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'zero', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ind', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'pair', Array, (0, None, (3,), name_type_map['Pair']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ind', name_type_map['Ushort'], (0, None), (False, None)
		yield 'pair', Array, (0, None, (3,), name_type_map['Pair']), (False, None)
