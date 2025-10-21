from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class LimbInfoZT(BaseStruct):

	"""
	32 bytes
	"""

	__name__ = 'LimbInfoZT'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.footplant = name_type_map['ChannelName'](self.context, 0, None)
		self.index_b = name_type_map['Ushort'](self.context, 0, None)
		self.zero_0 = name_type_map['Ushort'](self.context, 0, None)
		self.count_a = name_type_map['Ushort'](self.context, 0, None)
		self.count_b = name_type_map['Ushort'](self.context, 0, None)
		self.zero_1 = name_type_map['Ushort'](self.context, 0, None)
		self.zeros = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'footplant', name_type_map['ChannelName'], (0, None), (False, None), (None, None)
		yield 'index_b', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zero_0', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'count_a', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'count_b', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zero_1', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zeros', Array, (0, None, (5,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'footplant', name_type_map['ChannelName'], (0, None), (False, None)
		yield 'index_b', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zero_0', name_type_map['Ushort'], (0, None), (False, None)
		yield 'count_a', name_type_map['Ushort'], (0, None), (False, None)
		yield 'count_b', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zero_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zeros', Array, (0, None, (5,), name_type_map['Uint']), (False, None)
