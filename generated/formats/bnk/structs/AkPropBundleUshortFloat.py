from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkPropBundleUshortFloat(BaseStruct):

	__name__ = 'AkPropBundleUshortFloat'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.p_i_d = name_type_map['Ushort'](self.context, 0, None)
		self.p_value = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'p_i_d', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'p_value', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'p_i_d', name_type_map['Ushort'], (0, None), (False, None)
		yield 'p_value', name_type_map['Float'], (0, None), (False, None)
