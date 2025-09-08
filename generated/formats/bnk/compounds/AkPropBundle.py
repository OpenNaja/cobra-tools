from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkPropBundle(BaseStruct):

	__name__ = 'AkPropBundle'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.c_props = name_type_map['Ubyte'](self.context, 0, None)
		self.p_props = Array(self.context, 0, None, (0,), name_type_map['Byte'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'c_props', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'p_props', Array, (0, None, (None,), name_type_map['Byte']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'c_props', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'p_props', Array, (0, None, (instance.c_props,), name_type_map['Byte']), (False, None)
