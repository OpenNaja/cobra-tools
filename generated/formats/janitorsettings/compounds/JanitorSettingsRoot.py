from generated.formats.janitorsettings.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class JanitorSettingsRoot(MemStruct):

	"""
	huge batch of arrays at the head of the file
	"""

	__name__ = 'JanitorSettingsRoot'

	_import_key = 'janitorsettings.compounds.JanitorSettingsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0.0
		self.unk_1 = 0.0
		self.unk_2 = 0.0
		self.unk_3 = 0.0
		self.unk_4 = 0.0
		self.unk_5 = 0.0
		self.unk_6 = 0.0
		self.unk_7 = 0.0
		self.unk_8 = 0
		self.unk_9 = 0.0
		self.unk_10 = 0.0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.count_5 = 0
		self.count_6 = 0
		self.count_7 = 0
		self.count_8 = 0
		self.count_9 = 0
		self.count_10 = 0
		self.count_11 = 0
		self.count_12 = 0
		self.count_13 = 0
		self.count_14 = 0
		self.possibly_unused_count_0 = 0
		self.possibly_unused_count_1 = 0
		self.possibly_unused_count_2 = 0
		self.possibly_unused_count_3 = 0
		self.possibly_unused_count_4 = 0
		self.unk_11 = 0.0
		self.unk_12 = 0.0
		self.unk_13 = 0.0
		self.unk_14 = 0.0
		self.unk_15 = 0.0
		self.unk_16 = 0.0
		self.unk_17 = 0.0
		self.unk_18 = 0.0
		self.unk_19 = 0.0
		self.unk_20 = 0.0
		self.unk_21 = 0.0
		self.unk_22 = 0.0
		self.unk_23 = 0.0
		self.unk_24 = 0.0
		self.unk_25 = 0.0
		self.unk_26 = 0.0
		self.unk_27 = 0.0
		self.unk_28 = 0.0
		self.unk_29 = 0.0
		self.unk_30 = 0.0
		self.unk_31 = 0.0
		self.unk_32 = 0.0
		self.array_0 = name_type_map['ArrayPointer'](self.context, self.count_0, name_type_map['UIntPair'])
		self.array_1 = name_type_map['ArrayPointer'](self.context, self.count_1, name_type_map['UIntPair'])
		self.array_2 = name_type_map['ArrayPointer'](self.context, self.count_2, name_type_map['UIntPair'])
		self.array_3 = name_type_map['ArrayPointer'](self.context, self.count_3, name_type_map['UIntPair'])
		self.array_4 = name_type_map['ArrayPointer'](self.context, self.count_4, name_type_map['UIntPair'])
		self.array_5 = name_type_map['ArrayPointer'](self.context, self.count_5, name_type_map['UIntPair'])
		self.array_6 = name_type_map['ArrayPointer'](self.context, self.count_6, name_type_map['Uint'])
		self.array_7 = name_type_map['ArrayPointer'](self.context, self.count_7, name_type_map['Uint'])
		self.array_8 = name_type_map['ArrayPointer'](self.context, self.count_8, name_type_map['Uint'])
		self.array_9 = name_type_map['ArrayPointer'](self.context, self.count_9, name_type_map['Float'])
		self.array_10 = name_type_map['ArrayPointer'](self.context, self.count_10, name_type_map['Float'])
		self.array_11 = name_type_map['ArrayPointer'](self.context, self.count_11, name_type_map['Float'])
		self.array_12 = name_type_map['ArrayPointer'](self.context, self.count_12, name_type_map['Float'])
		self.array_13 = name_type_map['ArrayPointer'](self.context, self.count_13, name_type_map['Float'])
		self.array_14 = name_type_map['ArrayPointer'](self.context, self.count_14, name_type_map['Float'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('array_0', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_1', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_2', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_3', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_4', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_5', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_6', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_7', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_8', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_9', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_10', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_11', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_12', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_13', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('array_14', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None))
		yield ('unk_0', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_1', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_2', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_3', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_4', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_5', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_6', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_7', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_8', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('unk_9', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_10', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('count_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_3', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_4', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_5', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_6', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_7', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_8', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_9', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_10', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_11', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_12', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_13', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('count_14', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('possibly_unused_count_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('possibly_unused_count_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('possibly_unused_count_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('possibly_unused_count_3', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('possibly_unused_count_4', name_type_map['Ubyte'], (0, None), (False, None), (None, None))
		yield ('unk_11', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_12', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_13', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_14', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_15', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_16', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_17', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_18', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_19', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_20', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_21', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_22', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_23', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_24', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_25', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_26', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_27', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_28', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_29', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_30', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_31', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_32', name_type_map['Float'], (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'array_0', name_type_map['ArrayPointer'], (instance.count_0, name_type_map['UIntPair']), (False, None)
		yield 'array_1', name_type_map['ArrayPointer'], (instance.count_1, name_type_map['UIntPair']), (False, None)
		yield 'array_2', name_type_map['ArrayPointer'], (instance.count_2, name_type_map['UIntPair']), (False, None)
		yield 'array_3', name_type_map['ArrayPointer'], (instance.count_3, name_type_map['UIntPair']), (False, None)
		yield 'array_4', name_type_map['ArrayPointer'], (instance.count_4, name_type_map['UIntPair']), (False, None)
		yield 'array_5', name_type_map['ArrayPointer'], (instance.count_5, name_type_map['UIntPair']), (False, None)
		yield 'array_6', name_type_map['ArrayPointer'], (instance.count_6, name_type_map['Uint']), (False, None)
		yield 'array_7', name_type_map['ArrayPointer'], (instance.count_7, name_type_map['Uint']), (False, None)
		yield 'array_8', name_type_map['ArrayPointer'], (instance.count_8, name_type_map['Uint']), (False, None)
		yield 'array_9', name_type_map['ArrayPointer'], (instance.count_9, name_type_map['Float']), (False, None)
		yield 'array_10', name_type_map['ArrayPointer'], (instance.count_10, name_type_map['Float']), (False, None)
		yield 'array_11', name_type_map['ArrayPointer'], (instance.count_11, name_type_map['Float']), (False, None)
		yield 'array_12', name_type_map['ArrayPointer'], (instance.count_12, name_type_map['Float']), (False, None)
		yield 'array_13', name_type_map['ArrayPointer'], (instance.count_13, name_type_map['Float']), (False, None)
		yield 'array_14', name_type_map['ArrayPointer'], (instance.count_14, name_type_map['Float']), (False, None)
		yield 'unk_0', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_1', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_4', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_5', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_6', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_7', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_8', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_9', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_10', name_type_map['Float'], (0, None), (False, None)
		yield 'count_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_3', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_4', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_5', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_6', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_7', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_8', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_9', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_10', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_11', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_12', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_13', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_14', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'possibly_unused_count_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'possibly_unused_count_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'possibly_unused_count_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'possibly_unused_count_3', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'possibly_unused_count_4', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'unk_11', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_12', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_13', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_14', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_15', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_16', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_17', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_18', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_19', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_20', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_21', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_22', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_23', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_24', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_25', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_26', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_27', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_28', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_29', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_30', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_31', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_32', name_type_map['Float'], (0, None), (False, None)
