from generated.formats.casinolod.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class LodGroup(MemStruct):

	"""
	PC, JWE2 24 bytes
	"""

	__name__ = 'LodGroup'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.lods_count = name_type_map['Uint64'](self.context, 0, None)
		self.lod_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.lods = name_type_map['ArrayPointer'](self.context, self.lods_count, name_type_map['Lod'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'lod_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'lods', name_type_map['ArrayPointer'], (None, name_type_map['Lod']), (False, None), (None, None)
		yield 'lods_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'lod_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'lods', name_type_map['ArrayPointer'], (instance.lods_count, name_type_map['Lod']), (False, None)
		yield 'lods_count', name_type_map['Uint64'], (0, None), (False, None)
