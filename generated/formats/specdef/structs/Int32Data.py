from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.specdef.imports import name_type_map


class Int32Data(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'Int32Data'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = name_type_map['Int'](self.context, 0, None)
		self.imax = name_type_map['Int'](self.context, 0, None)
		self.ivalue = name_type_map['Int'](self.context, 0, None)
		self.ioptional = name_type_map['Int'](self.context, 0, None)
		self.enum = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'imin', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'imax', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'ivalue', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'ioptional', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'enum', name_type_map['Pointer'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'imin', name_type_map['Int'], (0, None), (False, None)
		yield 'imax', name_type_map['Int'], (0, None), (False, None)
		yield 'ivalue', name_type_map['Int'], (0, None), (False, None)
		yield 'ioptional', name_type_map['Int'], (0, None), (False, None)
		yield 'enum', name_type_map['Pointer'], (0, None), (False, None)
