from generated.formats.casinolod.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CasinoLodRoot(MemStruct):

	"""
	PZ, JWE2 32 bytes
	"""

	__name__ = 'CasinoLodRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.lod_groups_count = name_type_map['Uint64'](self.context, 0, None)
		self.zero = name_type_map['Uint64'].from_value(0)
		self.lod_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.lod_groups = name_type_map['ArrayPointer'](self.context, self.lod_groups_count, name_type_map['LodGroup'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'lod_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'lod_groups', name_type_map['ArrayPointer'], (None, name_type_map['LodGroup']), (False, None), (None, None)
		yield 'lod_groups_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (True, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'lod_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'lod_groups', name_type_map['ArrayPointer'], (instance.lod_groups_count, name_type_map['LodGroup']), (False, None)
		yield 'lod_groups_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (True, 0)
