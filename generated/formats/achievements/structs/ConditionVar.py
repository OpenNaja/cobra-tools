from generated.formats.achievements.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ConditionVar(MemStruct):

	"""
	PZ 32 bytes
	"""

	__name__ = 'ConditionVar'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.b = name_type_map['Uint64'](self.context, 0, None)
		self.count = name_type_map['Uint64'](self.context, 0, None)
		self.d = name_type_map['Uint64'](self.context, 0, None)
		self.condition_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'condition_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'b', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'd', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'condition_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'b', name_type_map['Uint64'], (0, None), (False, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'd', name_type_map['Uint64'], (0, None), (False, None)
