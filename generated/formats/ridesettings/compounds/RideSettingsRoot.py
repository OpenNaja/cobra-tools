from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ridesettings.imports import name_type_map


class RideSettingsRoot(MemStruct):

	"""
	PC 32 bytes
	PZ 16 bytes
	"""

	__name__ = 'RideSettingsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = name_type_map['Float'].from_value(0.4)
		self.unk_1 = name_type_map['Uint'](self.context, 0, None)
		self.count = name_type_map['Uint'](self.context, 0, None)
		self.pad_0 = name_type_map['Uint'](self.context, 0, None)
		self.pad_1 = name_type_map['Uint'](self.context, 0, None)
		self.pad_2 = name_type_map['Uint'](self.context, 0, None)
		self.array_1 = name_type_map['ArrayPointer'](self.context, self.count, name_type_map['Pair'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_0', name_type_map['Float'], (0, None), (False, 0.4), (None, None)
		yield 'unk_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'array_1', name_type_map['ArrayPointer'], (None, name_type_map['Pair']), (False, None), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'count', name_type_map['Uint'], (0, None), (False, None), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'pad_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'pad_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'pad_2', name_type_map['Uint'], (0, None), (False, None), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_0', name_type_map['Float'], (0, None), (False, 0.4)
		yield 'unk_1', name_type_map['Uint'], (0, None), (False, None)
		if not ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)):
			yield 'array_1', name_type_map['ArrayPointer'], (instance.count, name_type_map['Pair']), (False, None)
			yield 'count', name_type_map['Uint'], (0, None), (False, None)
		yield 'pad_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'pad_1', name_type_map['Uint'], (0, None), (False, None)
		if not ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)):
			yield 'pad_2', name_type_map['Uint'], (0, None), (False, None)
