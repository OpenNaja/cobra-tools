from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class GateInfo(MemStruct):

	__name__ = 'GateInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_ints_2 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.entrance = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.exit = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unk_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unk_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unk_3 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'entrance', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'exit', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_ints_2', Array, (0, None, (2,), name_type_map['Uint']), (False, None), (None, None)
		yield 'unk_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_3', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'entrance', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'exit', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_ints_2', Array, (0, None, (2,), name_type_map['Uint']), (False, None)
		yield 'unk_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_3', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None)
