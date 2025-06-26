from generated.array import Array
from generated.formats.frenderlodspec.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class LODGroup(MemStruct):

	"""
	PC 40 bytes
	PZ, JWE2 56 bytes
	"""

	__name__ = 'LODGroup'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.min_model_bounding_sphere_radius = name_type_map['Float'](self.context, 0, None)
		self.max_model_bounding_sphere_radius = name_type_map['Float'](self.context, 0, None)
		self.flags = name_type_map['Ushort'].from_value(255)
		self.lod_count = name_type_map['Ushort'].from_value(6)
		self.lod_points = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.pixel_size_off = name_type_map['Float'](self.context, 0, None)
		self.unused = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.group_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'group_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'min_model_bounding_sphere_radius', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'max_model_bounding_sphere_radius', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'flags', name_type_map['Ushort'], (0, None), (False, 255), (lambda context: not (context.version == 18), None)
		yield 'lod_count', name_type_map['Ushort'], (0, None), (False, 6), (lambda context: not (context.version == 18), None)
		yield 'lod_points', Array, (0, None, (5,), name_type_map['Float']), (False, None), (None, None)
		yield 'pixel_size_off', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unused', Array, (0, None, (3,), name_type_map['Uint']), (False, 0), (lambda context: not (context.version == 18), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'group_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'min_model_bounding_sphere_radius', name_type_map['Float'], (0, None), (False, None)
		yield 'max_model_bounding_sphere_radius', name_type_map['Float'], (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'flags', name_type_map['Ushort'], (0, None), (False, 255)
			yield 'lod_count', name_type_map['Ushort'], (0, None), (False, 6)
		yield 'lod_points', Array, (0, None, (5,), name_type_map['Float']), (False, None)
		yield 'pixel_size_off', name_type_map['Float'], (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'unused', Array, (0, None, (3,), name_type_map['Uint']), (False, 0)
