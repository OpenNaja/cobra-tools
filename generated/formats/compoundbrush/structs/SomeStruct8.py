from generated.formats.compoundbrush.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class SomeStruct8(MemStruct):

	__name__ = 'SomeStruct8'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unknown_byte = name_type_map['Byte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unknown_byte', name_type_map['Byte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unknown_byte', name_type_map['Byte'], (0, None), (False, None)
