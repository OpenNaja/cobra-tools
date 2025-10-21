from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.tex.imports import name_type_map


class TexelHeader(MemStruct):

	"""
	PC2: 8 bytes
	"""

	__name__ = 'TexelHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero = name_type_map['Uint64'].from_value(0)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'zero', name_type_map['Uint64'], (0, None), (True, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero', name_type_map['Uint64'], (0, None), (True, 0)
