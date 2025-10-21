from generated.formats.logicalcontrols.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class PCButtonData(MemStruct):

	"""
	#Specific for PC, the format is completely different
	"""

	__name__ = 'PCButtonData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.key_count = name_type_map['Ushort'](self.context, 0, None)
		self.key_flags = name_type_map['Ushort'](self.context, 0, None)
		self.unkown = name_type_map['Uint'](self.context, 0, None)
		self.keys = name_type_map['ArrayPointer'](self.context, self.key_count, name_type_map['ButtonStr'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'keys', name_type_map['ArrayPointer'], (None, name_type_map['ButtonStr']), (False, None), (None, None)
		yield 'key_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'key_flags', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unkown', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'keys', name_type_map['ArrayPointer'], (instance.key_count, name_type_map['ButtonStr']), (False, None)
		yield 'key_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'key_flags', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unkown', name_type_map['Uint'], (0, None), (False, None)
