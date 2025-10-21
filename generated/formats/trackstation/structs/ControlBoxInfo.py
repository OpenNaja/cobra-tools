from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class ControlBoxInfo(MemStruct):

	__name__ = 'ControlBoxInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.position = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.unkown_float_1 = name_type_map['Float'].from_value(0)
		self.unkown_float_2 = name_type_map['Float'].from_value(0)
		self.unkown_float_3 = name_type_map['Float'].from_value(0)
		self.unkown_float_4 = name_type_map['Float'].from_value(0)
		self.front_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.left_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.right_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'front_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'left_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'right_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'position', Array, (0, None, (3,), name_type_map['Float']), (False, None), (None, None)
		yield 'unkown_float_1', name_type_map['Float'], (0, None), (True, 0), (None, None)
		yield 'unkown_float_2', name_type_map['Float'], (0, None), (True, 0), (None, None)
		yield 'unkown_float_3', name_type_map['Float'], (0, None), (True, 0), (None, None)
		yield 'unkown_float_4', name_type_map['Float'], (0, None), (True, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'front_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'left_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'right_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'position', Array, (0, None, (3,), name_type_map['Float']), (False, None)
		yield 'unkown_float_1', name_type_map['Float'], (0, None), (True, 0)
		yield 'unkown_float_2', name_type_map['Float'], (0, None), (True, 0)
		yield 'unkown_float_3', name_type_map['Float'], (0, None), (True, 0)
		yield 'unkown_float_4', name_type_map['Float'], (0, None), (True, 0)
