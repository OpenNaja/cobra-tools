from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.researchdata.imports import name_type_map


class FxDataSettings(MemStruct):

	__name__ = 'FxDataSettings'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_1 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_2 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_3 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_4 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_5 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_6 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_7 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_ptr_0 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unk_ptr_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_ptr_0', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_ptr_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_4', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_5', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_6', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_7', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_ptr_0', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_ptr_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_4', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_5', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_6', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_7', name_type_map['Uint64'], (0, None), (False, None)
