from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ridesettings.imports import name_type_map


class RideSettingsRoot(MemStruct):

	__name__ = 'RideSettingsRoot'

	_import_key = 'ridesettings.compounds.RideSettingsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0.0
		self.unk_1 = 0
		self.count = 0
		self.pad_0 = 0
		self.pad_1 = 0
		self.pad_2 = 0
		self.array_1 = name_type_map['ArrayPointer'](self.context, self.count, name_type_map['Pair'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('unk_0', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_1', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('array_1', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('count', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('pad_0', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('pad_1', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('pad_2', name_type_map['Uint'], (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_0', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'array_1', name_type_map['ArrayPointer'], (instance.count, name_type_map['Pair']), (False, None)
		yield 'count', name_type_map['Uint'], (0, None), (False, None)
		yield 'pad_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'pad_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'pad_2', name_type_map['Uint'], (0, None), (False, None)
