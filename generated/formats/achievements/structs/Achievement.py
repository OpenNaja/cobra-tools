from generated.array import Array
from generated.formats.achievements.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Achievement(MemStruct):

	"""
	PZ 64 bytes
	"""

	__name__ = 'Achievement'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.conditions_count = name_type_map['Int'].from_value(1)
		self.minus_one_1 = name_type_map['Int'].from_value(-1)
		self.minus_one_2 = name_type_map['Int'].from_value(-1)
		self.zero_1 = name_type_map['Int'].from_value(0)
		self.zero_2 = name_type_map['Uint64'].from_value(0)
		self.flags = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.zero_3 = name_type_map['Int'].from_value(0)
		self.zero_4 = name_type_map['Uint64'].from_value(0)
		self.zero_5 = name_type_map['Uint64'].from_value(0)
		self.achievement_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.conditions = name_type_map['ArrayPointer'](self.context, self.conditions_count, name_type_map['ConditionRefPtr'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'achievement_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'conditions', name_type_map['ArrayPointer'], (None, name_type_map['ConditionRefPtr']), (False, None), (None, None)
		yield 'conditions_count', name_type_map['Int'], (0, None), (True, 1), (None, None)
		yield 'minus_one_1', name_type_map['Int'], (0, None), (True, -1), (None, None)
		yield 'minus_one_2', name_type_map['Int'], (0, None), (True, -1), (None, None)
		yield 'zero_1', name_type_map['Int'], (0, None), (True, 0), (None, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'flags', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'zero_3', name_type_map['Int'], (0, None), (True, 0), (None, None)
		yield 'zero_4', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'zero_5', name_type_map['Uint64'], (0, None), (True, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'achievement_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'conditions', name_type_map['ArrayPointer'], (instance.conditions_count, name_type_map['ConditionRefPtr']), (False, None)
		yield 'conditions_count', name_type_map['Int'], (0, None), (True, 1)
		yield 'minus_one_1', name_type_map['Int'], (0, None), (True, -1)
		yield 'minus_one_2', name_type_map['Int'], (0, None), (True, -1)
		yield 'zero_1', name_type_map['Int'], (0, None), (True, 0)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'flags', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None)
		yield 'zero_3', name_type_map['Int'], (0, None), (True, 0)
		yield 'zero_4', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'zero_5', name_type_map['Uint64'], (0, None), (True, 0)
