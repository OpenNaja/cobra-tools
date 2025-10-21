from generated.formats.achievements.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ConditionPc2(MemStruct):

	"""
	PC2 32 bytes
	PTR @ 352  -> SUB 117 | 7168 (  32)
	00 00 00 00 00 00 00 00 40 50 4F 49 4E 54 45 52  ........@POINTER
	00 00 40 40 00 00 00 00 00 00 00 00 00 00 00 00  ..@@............
	"""

	__name__ = 'ConditionPc2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = name_type_map['Uint64'](self.context, 0, None)
		self.b = name_type_map['Uint64'](self.context, 0, None)
		self.c = name_type_map['Uint64'](self.context, 0, None)
		self.reference = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'reference', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'c', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', name_type_map['Uint64'], (0, None), (False, None)
		yield 'reference', name_type_map['Pointer'], (0, None), (False, None)
		yield 'b', name_type_map['Uint64'], (0, None), (False, None)
		yield 'c', name_type_map['Uint64'], (0, None), (False, None)
