from generated.formats.accountlevelsdata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AccountLevelsDataRoot(MemStruct):

	__name__ = 'AccountLevelsDataRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.account_level_version = name_type_map['Uint64'](self.context, 0, None)
		self.account_levels_count = name_type_map['Uint64'](self.context, 0, None)
		self.account_levels = name_type_map['ArrayPointer'](self.context, self.account_levels_count, name_type_map['AccountLevel'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'account_level_version', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'account_levels', name_type_map['ArrayPointer'], (None, name_type_map['AccountLevel']), (False, None), (None, None)
		yield 'account_levels_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'account_level_version', name_type_map['Uint64'], (0, None), (False, None)
		yield 'account_levels', name_type_map['ArrayPointer'], (instance.account_levels_count, name_type_map['AccountLevel']), (False, None)
		yield 'account_levels_count', name_type_map['Uint64'], (0, None), (False, None)
