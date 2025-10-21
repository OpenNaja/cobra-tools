from generated.formats.dinosaurmaterialvariants.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Variant(MemStruct):

	__name__ = 'Variant'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.has_ptr = name_type_map['Uint64'](self.context, 0, None)
		self.variant_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'has_ptr', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'variant_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'has_ptr', name_type_map['Uint64'], (0, None), (False, None)
		yield 'variant_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
