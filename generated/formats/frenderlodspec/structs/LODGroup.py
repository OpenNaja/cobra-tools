from generated.formats.frenderlodspec.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class LODGroup(MemStruct):

	"""
	PC 40 bytes
	PZ, JWE2, PC2 56 bytes
	"""

	__name__ = 'LODGroup'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_float_1 = name_type_map['Float'].from_value(0.0)
		self.max_model_bounding_sphere_radius = name_type_map['Float'](self.context, 0, None)
		self.lod_points = name_type_map['LODPoints'](self.context, 0, None)
		self.sub_lod_points_count = name_type_map['Uint'].from_value(0)
		self.group_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.sub_lod_points = name_type_map['ArrayPointer'](self.context, self.sub_lod_points_count, name_type_map['LODPoints'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'group_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_float_1', name_type_map['Float'], (0, None), (True, 0.0), (None, None)
		yield 'max_model_bounding_sphere_radius', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'lod_points', name_type_map['LODPoints'], (0, None), (False, None), (None, None)
		yield 'sub_lod_points_count', name_type_map['Uint'], (0, None), (False, 0), (lambda context: not (context.version == 18), None)
		yield 'sub_lod_points', name_type_map['ArrayPointer'], (None, name_type_map['LODPoints']), (False, None), (lambda context: not (context.version == 18), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'group_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_float_1', name_type_map['Float'], (0, None), (True, 0.0)
		yield 'max_model_bounding_sphere_radius', name_type_map['Float'], (0, None), (False, None)
		yield 'lod_points', name_type_map['LODPoints'], (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'sub_lod_points_count', name_type_map['Uint'], (0, None), (False, 0)
			yield 'sub_lod_points', name_type_map['ArrayPointer'], (instance.sub_lod_points_count, name_type_map['LODPoints']), (False, None)
