from generated.formats.accountlevelsdata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AccountLevel(MemStruct):

	__name__ = 'AccountLevel'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.level_id = name_type_map['Uint64'](self.context, 0, None)
		self.levels_count = name_type_map['Uint64'](self.context, 0, None)
		self.levels = name_type_map['Pointer'](self.context, self.levels_count, name_type_map['ZStringList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'level_id', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'levels', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'levels_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'level_id', name_type_map['Uint64'], (0, None), (False, None)
		yield 'levels', name_type_map['Pointer'], (instance.levels_count, name_type_map['ZStringList']), (False, None)
		yield 'levels_count', name_type_map['Uint64'], (0, None), (False, None)
