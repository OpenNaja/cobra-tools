from generated.formats.dinosaurmaterialvariants.imports import name_type_map
from generated.formats.dinosaurmaterialvariants.structs.CommonHeader import CommonHeader


class DinoLayersHeader(CommonHeader):

	__name__ = 'DinoLayersHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.layer_count = name_type_map['Uint64'](self.context, 0, None)
		self.zero = name_type_map['Uint64'](self.context, 0, None)
		self.layers = name_type_map['ArrayPointer'](self.context, self.layer_count, name_type_map['Layer'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'layers', name_type_map['ArrayPointer'], (None, name_type_map['Layer']), (False, None), (None, None)
		yield 'layer_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'layers', name_type_map['ArrayPointer'], (instance.layer_count, name_type_map['Layer']), (False, None)
		yield 'layer_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (False, None)
