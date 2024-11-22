from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class ControlBoxInfo(MemStruct):

	__name__ = 'ControlBoxInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.front = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.mid = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.back = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'front', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'mid', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'back', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'floats', Array, (0, None, (7,), name_type_map['Float']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'front', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'mid', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'back', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'floats', Array, (0, None, (7,), name_type_map['Float']), (False, None)
