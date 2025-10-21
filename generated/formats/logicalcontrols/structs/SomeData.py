from generated.formats.logicalcontrols.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class SomeData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'SomeData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.key = name_type_map['Uint'](self.context, 0, None)
		self.extra = name_type_map['Uint'](self.context, 0, None)
		self.a = name_type_map['Float'](self.context, 0, None)
		self.b = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'key', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'extra', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'a', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'key', name_type_map['Uint'], (0, None), (False, None)
		yield 'extra', name_type_map['Uint'], (0, None), (False, None)
		yield 'a', name_type_map['Float'], (0, None), (False, None)
		yield 'b', name_type_map['Float'], (0, None), (False, None)
