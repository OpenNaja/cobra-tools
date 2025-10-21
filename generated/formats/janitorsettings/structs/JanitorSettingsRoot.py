from generated.array import Array
from generated.formats.janitorsettings.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class JanitorSettingsRoot(MemStruct):

	"""
	PC: 272 bytes, version 1
	PZ: 304 bytes, version 1
	PC2: 224 bytes, version 9
	"""

	__name__ = 'JanitorSettingsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.between_arrays = name_type_map['JanitorBetweenArrays'](self.context, 0, None)
		self.janitor_pre_count = name_type_map['JanitorPreCount'](self.context, 0, None)
		self.num_array_0 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_1 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_2 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_3 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_4 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_5 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_6 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_7 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_8 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_9 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_10 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_11 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_12 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_13 = name_type_map['Ubyte'](self.context, 0, None)
		self.num_array_14 = name_type_map['Ubyte'](self.context, 0, None)
		self.padding = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.janitor_end = name_type_map['JanitorEnd'](self.context, 0, None)
		self.array_0 = name_type_map['ArrayPointer'](self.context, self.num_array_0, name_type_map['Float'])
		self.array_1 = name_type_map['ArrayPointer'](self.context, self.num_array_1, name_type_map['Float'])
		self.array_2 = name_type_map['ArrayPointer'](self.context, self.num_array_2, name_type_map['Uint'])
		self.array_3 = name_type_map['ArrayPointer'](self.context, self.num_array_3, name_type_map['Float'])
		self.array_4 = name_type_map['ArrayPointer'](self.context, self.num_array_4, name_type_map['Float'])
		self.array_0 = name_type_map['ArrayPointer'](self.context, self.num_array_0, name_type_map['UIntPair'])
		self.array_1 = name_type_map['ArrayPointer'](self.context, self.num_array_1, name_type_map['UIntPair'])
		self.array_2 = name_type_map['ArrayPointer'](self.context, self.num_array_2, name_type_map['UIntPair'])
		self.array_3 = name_type_map['ArrayPointer'](self.context, self.num_array_3, name_type_map['UIntPair'])
		self.array_4 = name_type_map['ArrayPointer'](self.context, self.num_array_4, name_type_map['UIntPair'])
		self.array_5 = name_type_map['ArrayPointer'](self.context, self.num_array_5, name_type_map['UIntPair'])
		self.array_6 = name_type_map['ArrayPointer'](self.context, self.num_array_6, name_type_map['Uint'])
		self.array_7 = name_type_map['ArrayPointer'](self.context, self.num_array_7, name_type_map['Uint'])
		self.array_8 = name_type_map['ArrayPointer'](self.context, self.num_array_8, name_type_map['Uint'])
		self.array_9 = name_type_map['ArrayPointer'](self.context, self.num_array_9, name_type_map['Float'])
		self.array_10 = name_type_map['ArrayPointer'](self.context, self.num_array_10, name_type_map['Float'])
		self.array_11 = name_type_map['ArrayPointer'](self.context, self.num_array_11, name_type_map['Float'])
		self.array_12 = name_type_map['ArrayPointer'](self.context, self.num_array_12, name_type_map['Float'])
		self.array_13 = name_type_map['ArrayPointer'](self.context, self.num_array_13, name_type_map['Float'])
		self.array_14 = name_type_map['ArrayPointer'](self.context, self.num_array_14, name_type_map['Float'])
		self.array_pc_2 = name_type_map['ArrayPointer'](self.context, self.num_array_2, name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'array_0', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'array_1', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'array_2', name_type_map['ArrayPointer'], (None, name_type_map['Uint']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'array_3', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'array_4', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'array_0', name_type_map['ArrayPointer'], (None, name_type_map['UIntPair']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_1', name_type_map['ArrayPointer'], (None, name_type_map['UIntPair']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'between_arrays', name_type_map['JanitorBetweenArrays'], (0, None), (False, None), (lambda context: ((not context.user_version.use_djb) and (context.version >= 19)) and (not context.is_pc_2), None)
		yield 'array_2', name_type_map['ArrayPointer'], (None, name_type_map['UIntPair']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_3', name_type_map['ArrayPointer'], (None, name_type_map['UIntPair']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_4', name_type_map['ArrayPointer'], (None, name_type_map['UIntPair']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_5', name_type_map['ArrayPointer'], (None, name_type_map['UIntPair']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_6', name_type_map['ArrayPointer'], (None, name_type_map['Uint']), (False, None), (None, None)
		yield 'array_7', name_type_map['ArrayPointer'], (None, name_type_map['Uint']), (False, None), (None, None)
		yield 'array_8', name_type_map['ArrayPointer'], (None, name_type_map['Uint']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_9', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (None, None)
		yield 'array_10', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_11', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_12', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'array_13', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: context.version == 18, None)
		yield 'array_14', name_type_map['ArrayPointer'], (None, name_type_map['Float']), (False, None), (lambda context: context.version == 18, None)
		yield 'janitor_pre_count', name_type_map['JanitorPreCount'], (0, None), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'num_array_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_3', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_4', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_5', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'num_array_6', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_7', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_8', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'num_array_9', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_array_10', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'num_array_11', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'num_array_12', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'num_array_13', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version == 18, None)
		yield 'num_array_14', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version == 18, None)
		yield 'padding', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'padding', Array, (0, None, (7,), name_type_map['Ubyte']), (False, None), (lambda context: ((not context.user_version.use_djb) and (context.version >= 19)) and (not context.is_pc_2), None)
		yield 'padding', Array, (0, None, (5,), name_type_map['Ubyte']), (False, None), (lambda context: context.version == 18, None)
		yield 'array_pc_2', name_type_map['ArrayPointer'], (None, name_type_map['Uint']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'janitor_end', name_type_map['JanitorEnd'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.is_pc_2:
			yield 'array_0', name_type_map['ArrayPointer'], (instance.num_array_0, name_type_map['Float']), (False, None)
			yield 'array_1', name_type_map['ArrayPointer'], (instance.num_array_1, name_type_map['Float']), (False, None)
			yield 'array_2', name_type_map['ArrayPointer'], (instance.num_array_2, name_type_map['Uint']), (False, None)
			yield 'array_3', name_type_map['ArrayPointer'], (instance.num_array_3, name_type_map['Float']), (False, None)
			yield 'array_4', name_type_map['ArrayPointer'], (instance.num_array_4, name_type_map['Float']), (False, None)
		if not instance.context.is_pc_2:
			yield 'array_0', name_type_map['ArrayPointer'], (instance.num_array_0, name_type_map['UIntPair']), (False, None)
			yield 'array_1', name_type_map['ArrayPointer'], (instance.num_array_1, name_type_map['UIntPair']), (False, None)
		if ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)) and (not instance.context.is_pc_2):
			yield 'between_arrays', name_type_map['JanitorBetweenArrays'], (0, None), (False, None)
		if not instance.context.is_pc_2:
			yield 'array_2', name_type_map['ArrayPointer'], (instance.num_array_2, name_type_map['UIntPair']), (False, None)
			yield 'array_3', name_type_map['ArrayPointer'], (instance.num_array_3, name_type_map['UIntPair']), (False, None)
			yield 'array_4', name_type_map['ArrayPointer'], (instance.num_array_4, name_type_map['UIntPair']), (False, None)
			yield 'array_5', name_type_map['ArrayPointer'], (instance.num_array_5, name_type_map['UIntPair']), (False, None)
		yield 'array_6', name_type_map['ArrayPointer'], (instance.num_array_6, name_type_map['Uint']), (False, None)
		yield 'array_7', name_type_map['ArrayPointer'], (instance.num_array_7, name_type_map['Uint']), (False, None)
		if not instance.context.is_pc_2:
			yield 'array_8', name_type_map['ArrayPointer'], (instance.num_array_8, name_type_map['Uint']), (False, None)
		yield 'array_9', name_type_map['ArrayPointer'], (instance.num_array_9, name_type_map['Float']), (False, None)
		if not instance.context.is_pc_2:
			yield 'array_10', name_type_map['ArrayPointer'], (instance.num_array_10, name_type_map['Float']), (False, None)
			yield 'array_11', name_type_map['ArrayPointer'], (instance.num_array_11, name_type_map['Float']), (False, None)
			yield 'array_12', name_type_map['ArrayPointer'], (instance.num_array_12, name_type_map['Float']), (False, None)
		if instance.context.version == 18:
			yield 'array_13', name_type_map['ArrayPointer'], (instance.num_array_13, name_type_map['Float']), (False, None)
			yield 'array_14', name_type_map['ArrayPointer'], (instance.num_array_14, name_type_map['Float']), (False, None)
		if not instance.context.is_pc_2:
			yield 'janitor_pre_count', name_type_map['JanitorPreCount'], (0, None), (False, None)
		yield 'num_array_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_array_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_array_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_array_3', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_array_4', name_type_map['Ubyte'], (0, None), (False, None)
		if not instance.context.is_pc_2:
			yield 'num_array_5', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_array_6', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_array_7', name_type_map['Ubyte'], (0, None), (False, None)
		if not instance.context.is_pc_2:
			yield 'num_array_8', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_array_9', name_type_map['Ubyte'], (0, None), (False, None)
		if not instance.context.is_pc_2:
			yield 'num_array_10', name_type_map['Ubyte'], (0, None), (False, None)
			yield 'num_array_11', name_type_map['Ubyte'], (0, None), (False, None)
			yield 'num_array_12', name_type_map['Ubyte'], (0, None), (False, None)
		if instance.context.version == 18:
			yield 'num_array_13', name_type_map['Ubyte'], (0, None), (False, None)
			yield 'num_array_14', name_type_map['Ubyte'], (0, None), (False, None)
		if instance.context.is_pc_2:
			yield 'padding', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None)
		if ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)) and (not instance.context.is_pc_2):
			yield 'padding', Array, (0, None, (7,), name_type_map['Ubyte']), (False, None)
		if instance.context.version == 18:
			yield 'padding', Array, (0, None, (5,), name_type_map['Ubyte']), (False, None)
		if instance.context.is_pc_2:
			yield 'array_pc_2', name_type_map['ArrayPointer'], (instance.num_array_2, name_type_map['Uint']), (False, None)
		yield 'janitor_end', name_type_map['JanitorEnd'], (0, None), (False, None)
