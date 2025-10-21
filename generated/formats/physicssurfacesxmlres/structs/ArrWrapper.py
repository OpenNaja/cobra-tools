from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class ArrWrapper(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'ArrWrapper'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = name_type_map['Ushort'](self.context, 0, None)
		self.flag = name_type_map['Ushort'](self.context, 0, None)
		self.unk = name_type_map['Uint'](self.context, 0, None)
		self.arr = name_type_map['ArrayPointer'](self.context, self.count, self.template)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'arr', name_type_map['ArrayPointer'], (None, None), (False, None), (None, None)
		yield 'count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'flag', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'arr', name_type_map['ArrayPointer'], (instance.count, instance.template), (False, None)
		yield 'count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'flag', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk', name_type_map['Uint'], (0, None), (False, None)
