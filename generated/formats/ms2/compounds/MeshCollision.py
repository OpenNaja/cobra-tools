import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint64
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.SubA import SubA
from generated.formats.ms2.compounds.SubCollChunk import SubCollChunk
from generated.formats.ms2.compounds.Vector3 import Vector3
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class MeshCollision(BaseStruct):

	"""
	JWE2: 188 bytes
	"""

	__name__ = 'MeshCollision'

	_import_key = 'ms2.compounds.MeshCollision'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rotation = Matrix33(self.context, 0, None)

		# offset of mesh
		self.offset = Vector3(self.context, 0, None)

		# shared among (all?) redwoods
		self.unk_1 = Array(self.context, 0, None, (0,), SubA)

		# vertices (3 float)
		self.vertex_count = 0

		# tris?, counts the 25s at the end
		self.tri_count = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, 0, None)

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, 0, None)
		self.flag_0 = 1
		self.flag_1 = 1
		self.has_sub_coll_chunk = 0
		self.zeros_1 = Array(self.context, 0, None, (0,), Uint64)
		self.ff = -1
		self.zeros_2 = Array(self.context, 0, None, (0,), Int)

		# sometimes 8 bytes, apparently not part of SubCollChunk (JWE2 dev footplantingtest_ has that but not the padding)
		self.weird_padding = SmartPadding(self.context, 4, None)

		# seems to repeat tri_count
		self.sub_coll_chunk = SubCollChunk(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('rotation', Matrix33, (0, None), (False, None), None)
		yield ('offset', Vector3, (0, None), (False, None), None)
		yield ('unk_1', Array, (0, None, (3,), SubA), (False, None), None)
		yield ('vertex_count', Uint64, (0, None), (False, None), None)
		yield ('tri_count', Uint64, (0, None), (False, None), None)
		yield ('bounds_min', Vector3, (0, None), (False, None), None)
		yield ('bounds_max', Vector3, (0, None), (False, None), None)
		yield ('flag_0', Uint64, (0, None), (False, 1), None)
		yield ('flag_1', Uint64, (0, None), (False, 1), None)
		yield ('has_sub_coll_chunk', Uint64, (0, None), (False, None), None)
		yield ('zeros_1', Array, (0, None, (4,), Uint64), (False, None), None)
		yield ('ff', Int, (0, None), (False, -1), None)
		yield ('zeros_2', Array, (0, None, (7,), Int), (False, None), None)
		yield ('weird_padding', SmartPadding, (4, None), (False, None), None)
		yield ('sub_coll_chunk', SubCollChunk, (0, None), (False, None), True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rotation', Matrix33, (0, None), (False, None)
		yield 'offset', Vector3, (0, None), (False, None)
		yield 'unk_1', Array, (0, None, (3,), SubA), (False, None)
		yield 'vertex_count', Uint64, (0, None), (False, None)
		yield 'tri_count', Uint64, (0, None), (False, None)
		yield 'bounds_min', Vector3, (0, None), (False, None)
		yield 'bounds_max', Vector3, (0, None), (False, None)
		yield 'flag_0', Uint64, (0, None), (False, 1)
		yield 'flag_1', Uint64, (0, None), (False, 1)
		yield 'has_sub_coll_chunk', Uint64, (0, None), (False, None)
		yield 'zeros_1', Array, (0, None, (4,), Uint64), (False, None)
		yield 'ff', Int, (0, None), (False, -1)
		yield 'zeros_2', Array, (0, None, (7,), Int), (False, None)
		yield 'weird_padding', SmartPadding, (4, None), (False, None)
		if instance.has_sub_coll_chunk:
			yield 'sub_coll_chunk', SubCollChunk, (0, None), (False, None)


MeshCollision.init_attributes()
