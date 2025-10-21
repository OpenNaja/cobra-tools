from generated.formats.achievements.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ConditionRef2(MemStruct):

	"""
	PZ 64, or probably 48 bytes
	"""

	__name__ = 'ConditionRef2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mode = name_type_map['Uint64'](self.context, 0, None)
		self.count = name_type_map['Uint64'].from_value(1)
		self.zero_1 = name_type_map['Uint64'].from_value(0)
		self.zero_2 = name_type_map['Uint64'].from_value(0)
		self.ref_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.condition_ref = name_type_map['Pointer'](self.context, 0, name_type_map['ConditionRef'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'mode', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'condition_ref', name_type_map['Pointer'], (0, name_type_map['ConditionRef']), (False, None), (None, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, 1), (None, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'mode', name_type_map['Uint64'], (0, None), (False, None)
		yield 'condition_ref', name_type_map['Pointer'], (0, name_type_map['ConditionRef']), (False, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, 1)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0)
