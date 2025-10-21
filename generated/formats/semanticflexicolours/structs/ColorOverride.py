from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.semanticflexicolours.imports import name_type_map


class ColorOverride(MemStruct):

	"""
	PZ: 24 bytes
	"""

	__name__ = 'ColorOverride'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.color = name_type_map['FloatColor'](self.context, 0, None)
		self.flexi_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'flexi_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'color', name_type_map['FloatColor'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'flexi_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'color', name_type_map['FloatColor'], (0, None), (False, None)
