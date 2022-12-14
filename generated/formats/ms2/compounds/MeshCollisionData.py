import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.Empty import Empty


class MeshCollisionData(BaseStruct):

	__name__ = 'MeshCollisionData'

	_import_key = 'ms2.compounds.MeshCollisionData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# usually zero, nonzero in JWE2 dev footplant, [1] used as salt for tri indices
		self.tris_salt = Array(self.context, 0, None, (0,), Uint)
		self.vertices_addr = Empty(self.context, 0, None)

		# array of vertices
		self.vertices = Array(self.context, 0, None, (0,), Float)
		self.triangles_addr = Empty(self.context, 0, None)

		# triangle indices into vertex list
		self.triangles = Array(self.context, 0, None, (0,), Ushort)

		# ?
		self.const = 0

		# in JWE1 redwood: always 37
		self.triangle_flags = Array(self.context, 0, None, (0,), Uint)

		# might be padding!
		self.zero_end = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('tris_salt', Array, (0, None, (4,), Uint), (False, None), True),
		('vertices_addr', Empty, (0, None), (False, None), None),
		('vertices', Array, (0, None, (None, 3,), Float), (False, None), None),
		('triangles_addr', Empty, (0, None), (False, None), None),
		('triangles', Array, (0, None, (None, 3,), Ushort), (False, None), None),
		('const', Uint, (0, None), (False, None), True),
		('triangle_flags', Array, (0, None, (None,), Uint), (False, None), True),
		('zero_end', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg.has_sub_coll_chunk:
			yield 'tris_salt', Array, (0, None, (4,), Uint), (False, None)
		yield 'vertices_addr', Empty, (0, None), (False, None)
		yield 'vertices', Array, (0, None, (instance.arg.vertex_count, 3,), Float), (False, None)
		yield 'triangles_addr', Empty, (0, None), (False, None)
		yield 'triangles', Array, (0, None, (instance.arg.tri_count, 3,), Ushort), (False, None)
		if instance.context.version <= 47:
			yield 'const', Uint, (0, None), (False, None)
		if instance.context.version <= 47 and instance.const:
			yield 'triangle_flags', Array, (0, None, (instance.arg.tri_flags_count,), Uint), (False, None)
		yield 'zero_end', Uint, (0, None), (False, None)
