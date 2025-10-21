from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class OnlyName(MemStruct):

	"""
	PC, JWE1: 16 bytes
	"""

	__name__ = 'OnlyName'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.index = name_type_map['Uint64'](self.context, 0, None)
		self.name_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'index', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'index', name_type_map['Uint64'], (0, None), (False, None)
