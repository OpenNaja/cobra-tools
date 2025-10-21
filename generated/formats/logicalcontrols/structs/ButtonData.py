from generated.formats.logicalcontrols.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ButtonData(MemStruct):

	__name__ = 'ButtonData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.k_1_a = name_type_map['Ushort'](self.context, 0, None)
		self.k_1_b = name_type_map['Ushort'](self.context, 0, None)
		self.k_2 = name_type_map['Uint'](self.context, 0, None)
		self.k_3 = name_type_map['Uint'](self.context, 0, None)
		self.k_4 = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'k_1_a', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'k_1_b', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'k_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'k_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'k_4', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'k_1_a', name_type_map['Ushort'], (0, None), (False, None)
		yield 'k_1_b', name_type_map['Ushort'], (0, None), (False, None)
		yield 'k_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'k_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'k_4', name_type_map['Uint'], (0, None), (False, None)
