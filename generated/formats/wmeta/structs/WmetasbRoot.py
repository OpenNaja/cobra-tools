from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.wmeta.imports import name_type_map


class WmetasbRoot(MemStruct):

	__name__ = 'WmetasbRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.bnks_count = name_type_map['Uint64'](self.context, 0, None)
		self.bnks = name_type_map['ArrayPointer'](self.context, self.bnks_count, name_type_map['BnkMeta'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'bnks', name_type_map['ArrayPointer'], (None, name_type_map['BnkMetaNew']), (False, None), (lambda context: context.version >= 2, None)
		yield 'bnks', name_type_map['ArrayPointer'], (None, name_type_map['BnkMeta']), (False, None), (lambda context: context.version <= 1, None)
		yield 'bnks_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 2:
			yield 'bnks', name_type_map['ArrayPointer'], (instance.bnks_count, name_type_map['BnkMetaNew']), (False, None)
		if instance.context.version <= 1:
			yield 'bnks', name_type_map['ArrayPointer'], (instance.bnks_count, name_type_map['BnkMeta']), (False, None)
		yield 'bnks_count', name_type_map['Uint64'], (0, None), (False, None)
