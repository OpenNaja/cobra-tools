from generated.formats.frenderlodspec.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FRenderLodSpecRoot(MemStruct):

	"""
	PZ, JWE2 16 bytes
	"""

	__name__ = 'FRenderLodSpecRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.lod_groups_count = name_type_map['Uint64'](self.context, 0, None)
		self.lod_groups = name_type_map['ArrayPointer'](self.context, self.lod_groups_count, name_type_map['LODGroup'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'lod_groups', name_type_map['ArrayPointer'], (None, name_type_map['LODGroup']), (False, None), (None, None)
		yield 'lod_groups_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'lod_groups', name_type_map['ArrayPointer'], (instance.lod_groups_count, name_type_map['LODGroup']), (False, None)
		yield 'lod_groups_count', name_type_map['Uint64'], (0, None), (False, None)
