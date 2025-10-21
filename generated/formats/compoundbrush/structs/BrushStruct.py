from generated.formats.compoundbrush.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BrushStruct(MemStruct):

	__name__ = 'BrushStruct'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding = name_type_map['Uint64'](self.context, 0, None)
		self.brush_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.index = name_type_map['Pointer'](self.context, 0, name_type_map['BrushIndex'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'brush_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'index', name_type_map['Pointer'], (0, name_type_map['BrushIndex']), (False, None), (None, None)
		yield 'padding', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'brush_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'index', name_type_map['Pointer'], (0, name_type_map['BrushIndex']), (False, None)
		yield 'padding', name_type_map['Uint64'], (0, None), (False, None)
