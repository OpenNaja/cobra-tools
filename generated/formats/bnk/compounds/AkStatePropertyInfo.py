from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkStatePropertyInfo(BaseStruct):

	__name__ = 'AkStatePropertyInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.property_id = name_type_map['Ubyte'](self.context, 0, None)
		self.accum_type = name_type_map['Ubyte'](self.context, 0, None)
		self.in_db = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'property_id', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'accum_type', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'in_db', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'property_id', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'accum_type', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'in_db', name_type_map['Ubyte'], (0, None), (False, None)
