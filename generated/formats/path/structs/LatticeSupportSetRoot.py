from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.path.imports import name_type_map


class LatticeSupportSetRoot(MemStruct):

	__name__ = 'LatticeSupportSetRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.num_sub_brace = name_type_map['Uint64'](self.context, 0, None)
		self.num_data = name_type_map['Uint64'](self.context, 0, None)
		self.padding = name_type_map['Uint64'](self.context, 0, None)
		self.model_00 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.model_08 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.model_16 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.model_24 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.sub_braces = name_type_map['ArrayPointer'](self.context, self.num_sub_brace, name_type_map['SubBrace'])
		self.data = name_type_map['ArrayPointer'](self.context, self.num_data, name_type_map['SupportSetData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'model_00', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'model_08', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'model_16', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'model_24', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_floats', Array, (0, None, (10,), name_type_map['Float']), (False, None), (None, None)
		yield 'sub_braces', name_type_map['ArrayPointer'], (None, name_type_map['SubBrace']), (False, None), (None, None)
		yield 'num_sub_brace', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data', name_type_map['ArrayPointer'], (None, name_type_map['SupportSetData']), (False, None), (None, None)
		yield 'num_data', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'padding', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'model_00', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'model_08', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'model_16', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'model_24', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_floats', Array, (0, None, (10,), name_type_map['Float']), (False, None)
		yield 'sub_braces', name_type_map['ArrayPointer'], (instance.num_sub_brace, name_type_map['SubBrace']), (False, None)
		yield 'num_sub_brace', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data', name_type_map['ArrayPointer'], (instance.num_data, name_type_map['SupportSetData']), (False, None)
		yield 'num_data', name_type_map['Uint64'], (0, None), (False, None)
		yield 'padding', name_type_map['Uint64'], (0, None), (False, None)
