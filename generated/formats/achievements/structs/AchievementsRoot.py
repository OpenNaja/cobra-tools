from generated.formats.achievements.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AchievementsRoot(MemStruct):

	"""
	PZ: 48 bytes
	PC2: 32 bytes
	"""

	__name__ = 'AchievementsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.condition_vars_count = name_type_map['Uint64'](self.context, 0, None)
		self.condition_checks_count = name_type_map['Uint64'](self.context, 0, None)
		self.c_count = name_type_map['Uint64'](self.context, 0, None)
		self.condition_vars = name_type_map['ArrayPointer'](self.context, self.condition_vars_count, name_type_map['ConditionVarPtr'])
		self.condition_checks = name_type_map['ArrayPointer'](self.context, self.condition_checks_count, name_type_map['ConditionCheck'])
		self.c = name_type_map['ArrayPointer'](self.context, self.c_count, name_type_map['Achievement'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'condition_vars', name_type_map['ArrayPointer'], (None, name_type_map['ConditionVarPtr']), (False, None), (None, None)
		yield 'condition_vars_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'condition_checks', name_type_map['ArrayPointer'], (None, name_type_map['ConditionCheck']), (False, None), (None, None)
		yield 'condition_checks_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'c', name_type_map['ArrayPointer'], (None, name_type_map['Achievement']), (False, None), (lambda context: context.version <= 3, None)
		yield 'c_count', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version <= 3, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'condition_vars', name_type_map['ArrayPointer'], (instance.condition_vars_count, name_type_map['ConditionVarPtr']), (False, None)
		yield 'condition_vars_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'condition_checks', name_type_map['ArrayPointer'], (instance.condition_checks_count, name_type_map['ConditionCheck']), (False, None)
		yield 'condition_checks_count', name_type_map['Uint64'], (0, None), (False, None)
		if instance.context.version <= 3:
			yield 'c', name_type_map['ArrayPointer'], (instance.c_count, name_type_map['Achievement']), (False, None)
			yield 'c_count', name_type_map['Uint64'], (0, None), (False, None)
