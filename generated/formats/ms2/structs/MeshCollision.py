from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class MeshCollision(BaseStruct):

	"""
	JWE2: 188 bytes
	"""

	__name__ = 'MeshCollision'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rotation = name_type_map['Matrix33'](self.context, 0, None)

		# offset of mesh
		self.offset = name_type_map['Vector3'](self.context, 0, None)

		# seems to be constant
		self.indices = Array(self.context, 0, None, (0,), name_type_map['MeshCollisionIndex'])

		# found in PC FR_GrandCarousel
		self.unk_2 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.vertex_count = name_type_map['Uint64'](self.context, 0, None)
		self.tri_count = name_type_map['Uint64'](self.context, 0, None)

		# the smallest coordinates across all axes
		self.bounds_min = name_type_map['Vector3'](self.context, 0, None)

		# the biggest coordinates across all axes
		self.bounds_max = name_type_map['Vector3'](self.context, 0, None)
		self.flag_0 = name_type_map['Uint64'].from_value(1)
		self.flag_1 = name_type_map['Uint64'].from_value(1)

		# seen 1 eg PZ widgetball_test_, or 0 in JWE2 characterscale and PZ CM_Common_Roofs
		self.is_optimized = name_type_map['Uint64'](self.context, 0, None)
		self.zeros_1 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.tris_switch = name_type_map['Uint64'](self.context, 0, None)
		self.ff = name_type_map['Int'].from_value(-1)
		self.zeros_2 = Array(self.context, 0, None, (0,), name_type_map['Int'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'rotation', name_type_map['Matrix33'], (0, None), (False, None), (None, None)
		yield 'offset', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'indices', Array, (0, None, (3,), name_type_map['MeshCollisionIndex']), (False, None), (None, None)
		yield 'unk_2', Array, (0, None, (3,), name_type_map['Uint']), (False, None), (lambda context: context.version == 32, None)
		yield 'vertex_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'tri_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'bounds_min', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'bounds_max', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'flag_0', name_type_map['Uint64'], (0, None), (False, 1), (None, None)
		yield 'flag_1', name_type_map['Uint64'], (0, None), (False, 1), (None, None)
		yield 'is_optimized', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zeros_1', Array, (0, None, (3,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'tris_switch', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ff', name_type_map['Int'], (0, None), (False, -1), (None, None)
		yield 'zeros_2', Array, (0, None, (7,), name_type_map['Int']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rotation', name_type_map['Matrix33'], (0, None), (False, None)
		yield 'offset', name_type_map['Vector3'], (0, None), (False, None)
		yield 'indices', Array, (0, None, (3,), name_type_map['MeshCollisionIndex']), (False, None)
		if instance.context.version == 32:
			yield 'unk_2', Array, (0, None, (3,), name_type_map['Uint']), (False, None)
		yield 'vertex_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'tri_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'bounds_min', name_type_map['Vector3'], (0, None), (False, None)
		yield 'bounds_max', name_type_map['Vector3'], (0, None), (False, None)
		yield 'flag_0', name_type_map['Uint64'], (0, None), (False, 1)
		yield 'flag_1', name_type_map['Uint64'], (0, None), (False, 1)
		yield 'is_optimized', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zeros_1', Array, (0, None, (3,), name_type_map['Uint64']), (False, None)
		yield 'tris_switch', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ff', name_type_map['Int'], (0, None), (False, -1)
		yield 'zeros_2', Array, (0, None, (7,), name_type_map['Int']), (False, None)
