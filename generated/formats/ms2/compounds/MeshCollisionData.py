from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class MeshCollisionData(BaseStruct):

	__name__ = 'MeshCollisionData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.optimizer = name_type_map['MeshCollisionOptimizer'](self.context, 0, None)
		self.vertices_addr = name_type_map['Empty'](self.context, 0, None)

		# array of vertices
		self.vertices = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.triangles_addr = name_type_map['Empty'](self.context, 0, None)

		# triangle indices into vertex list
		self.triangles = Array(self.context, 0, None, (0,), name_type_map['Ushort'])

		# ?; PC: 32
		self.const = name_type_map['Uint'](self.context, 0, None)

		# in JWE redwood: always 37
		self.triangle_flags = Array(self.context, 0, None, (0,), name_type_map['Uint'])

		# ?
		self.triangle_flags_pc = Array(self.context, 0, None, (0,), name_type_map['Short'])
		self.mesh_aligner = name_type_map['PadAlign'](self.context, 8, self.vertices_addr)

		# JWE2 LAG_NaturalWaterPool_Malta_Walls
		self.zero_end = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'optimizer', name_type_map['MeshCollisionOptimizer'], (0, None), (False, None), (None, True)
		yield 'vertices_addr', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'vertices', Array, (0, None, (None, 3,), name_type_map['Float']), (False, None), (None, None)
		yield 'triangles_addr', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'triangles', Array, (0, None, (None, 3,), name_type_map['Ushort']), (False, None), (None, None)
		yield 'const', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version <= 47, None)
		yield 'triangle_flags', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (lambda context: context.version <= 47 and not (context.version == 32), True)
		yield 'triangle_flags_pc', Array, (0, None, (None, 2,), name_type_map['Short']), (False, None), (lambda context: context.version == 32, True)
		yield 'mesh_aligner', name_type_map['PadAlign'], (8, None), (False, None), (lambda context: context.version <= 32, None)
		yield 'zero_end', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 52, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg.is_optimized:
			yield 'optimizer', name_type_map['MeshCollisionOptimizer'], (0, None), (False, None)
		yield 'vertices_addr', name_type_map['Empty'], (0, None), (False, None)
		yield 'vertices', Array, (0, None, (instance.arg.vertex_count, 3,), name_type_map['Float']), (False, None)
		yield 'triangles_addr', name_type_map['Empty'], (0, None), (False, None)
		yield 'triangles', Array, (0, None, (instance.arg.tri_count, 3,), name_type_map['Ushort']), (False, None)
		if instance.context.version <= 47:
			yield 'const', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version <= 47 and not (instance.context.version == 32) and instance.const:
			yield 'triangle_flags', Array, (0, None, (instance.optimizer.tri_flags_count,), name_type_map['Uint']), (False, None)
		if instance.context.version == 32 and instance.arg.tris_switch:
			yield 'triangle_flags_pc', Array, (0, None, (instance.arg.tri_count, 2,), name_type_map['Short']), (False, None)
		if instance.context.version <= 32:
			yield 'mesh_aligner', name_type_map['PadAlign'], (8, instance.vertices_addr), (False, None)
		if instance.context.version >= 52:
			yield 'zero_end', name_type_map['Uint'], (0, None), (False, None)
