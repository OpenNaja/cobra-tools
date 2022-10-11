import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.MeshCollisionBit import MeshCollisionBit
from generated.formats.ms2.compounds.Vector3 import Vector3


class MeshCollision(BaseStruct):

	__name__ = 'MeshCollision'

	_import_key = 'ms2.compounds.MeshCollision'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rotation = Matrix33(self.context, 0, None)

		# offset of mesh
		self.offset = Vector3(self.context, 0, None)

		# not floats, maybe 6 ushorts, shared among (all?) redwoods
		self.unk_1 = Array(self.context, 0, None, (0,), Ushort)

		# vertices (3 float)
		self.vertex_count = 0

		# tris?, counts the 25s at the end
		self.tri_count = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, 0, None)

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, 0, None)

		# seemingly fixed
		self.ones_or_zeros = Array(self.context, 0, None, (0,), Uint64)

		# seemingly fixed
		self.ff_or_zero = Array(self.context, 0, None, (0,), Int)

		# verbatim
		self.bounds_min_repeat = Vector3(self.context, 0, None)

		# verbatim
		self.bounds_max_repeat = Vector3(self.context, 0, None)

		# seems to repeat tri_count
		self.tri_flags_count = 0

		# counts MeshCollisionBit
		self.count_bits = 0

		# ?
		self.stuff = Array(self.context, 0, None, (0,), Ushort)

		# ?
		self.collision_bits = Array(self.context, 0, None, (0,), MeshCollisionBit)

		# always 25
		self.zeros = Array(self.context, 0, None, (0,), Uint)

		# array of vertices
		self.vertices = Array(self.context, 0, None, (0,), Float)

		# triangle indices into vertex list
		self.triangles = Array(self.context, 0, None, (0,), Ushort)

		# ?
		self.const = 0

		# always 25
		self.triangle_flags = Array(self.context, 0, None, (0,), Uint)

		# might be padding!
		self.zero_end = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('rotation', Matrix33, (0, None), (False, None), None),
		('offset', Vector3, (0, None), (False, None), None),
		('unk_1', Array, (0, None, (3, 2,), Ushort), (False, None), None),
		('vertex_count', Uint64, (0, None), (False, None), None),
		('tri_count', Uint64, (0, None), (False, None), None),
		('bounds_min', Vector3, (0, None), (False, None), None),
		('bounds_max', Vector3, (0, None), (False, None), None),
		('ones_or_zeros', Array, (0, None, (7,), Uint64), (False, None), None),
		('ff_or_zero', Array, (0, None, (10,), Int), (False, None), True),
		('ff_or_zero', Array, (0, None, (8,), Int), (False, None), True),
		('bounds_min_repeat', Vector3, (0, None), (False, None), True),
		('bounds_max_repeat', Vector3, (0, None), (False, None), True),
		('tri_flags_count', Uint, (0, None), (False, None), True),
		('count_bits', Ushort, (0, None), (False, None), True),
		('stuff', Array, (0, None, (9,), Ushort), (False, None), True),
		('collision_bits', Array, (0, None, (None,), MeshCollisionBit), (False, None), True),
		('zeros', Array, (0, None, (4,), Uint), (False, None), True),
		('vertices', Array, (0, None, (None, 3,), Float), (False, None), None),
		('triangles', Array, (0, None, (None, 3,), Ushort), (False, None), None),
		('const', Uint, (0, None), (False, None), True),
		('triangle_flags', Array, (0, None, (None,), Uint), (False, None), True),
		('zero_end', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rotation', Matrix33, (0, None), (False, None)
		yield 'offset', Vector3, (0, None), (False, None)
		yield 'unk_1', Array, (0, None, (3, 2,), Ushort), (False, None)
		yield 'vertex_count', Uint64, (0, None), (False, None)
		yield 'tri_count', Uint64, (0, None), (False, None)
		yield 'bounds_min', Vector3, (0, None), (False, None)
		yield 'bounds_max', Vector3, (0, None), (False, None)
		yield 'ones_or_zeros', Array, (0, None, (7,), Uint64), (False, None)
		if instance.context.version <= 32:
			yield 'ff_or_zero', Array, (0, None, (10,), Int), (False, None)
		if instance.context.version >= 47:
			yield 'ff_or_zero', Array, (0, None, (8,), Int), (False, None)
		if instance.context.version <= 32:
			yield 'bounds_min_repeat', Vector3, (0, None), (False, None)
			yield 'bounds_max_repeat', Vector3, (0, None), (False, None)
			yield 'tri_flags_count', Uint, (0, None), (False, None)
			yield 'count_bits', Ushort, (0, None), (False, None)
			yield 'stuff', Array, (0, None, (9,), Ushort), (False, None)
			yield 'collision_bits', Array, (0, None, (instance.count_bits,), MeshCollisionBit), (False, None)
			yield 'zeros', Array, (0, None, (4,), Uint), (False, None)
		yield 'vertices', Array, (0, None, (instance.vertex_count, 3,), Float), (False, None)
		yield 'triangles', Array, (0, None, (instance.tri_count, 3,), Ushort), (False, None)
		if instance.context.version <= 32:
			yield 'const', Uint, (0, None), (False, None)
		if instance.context.version <= 32 and instance.const:
			yield 'triangle_flags', Array, (0, None, (instance.tri_flags_count,), Uint), (False, None)
		yield 'zero_end', Uint, (0, None), (False, None)
