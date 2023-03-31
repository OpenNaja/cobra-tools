from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class LodInfo(BaseStruct):

	"""
	DLA, ZTUAC - 16 bytes
	JWE1, PZ, JWE2 - 20 bytes
	JWE2 Biosyn - 12 bytes, skips the vert / tris counts
	"""

	__name__ = 'LodInfo'

	_import_key = 'ms2.compounds.LodInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# FFFF
		self.full = 0

		# 7F7F
		self.half = 0

		# increasing
		self.lod_index = 0

		# usually first lod is 900
		self.distance = 0.0

		# matches the buffer index used by this LOD's meshes
		self.stream_index = 0

		# Last bone that is used by this lod's models; usually decreases with increasing lod index to decimate bones. However: JWE detailobjects - nat_groundcover_searocket_patchy_02 due to dedicated lod nodes
		self.bone_index = 0

		# first object for this lod in objects list
		self.first_object_index = 0
		self.first_object_index_1 = 0
		self.first_object_index_2 = 0

		# not included in interval (python style indexing)
		self.last_object_index = 0

		# vertex count of lod, sum of all vertex counts that are attached to this lod; rendered count, including duped models
		self.vertex_count = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer); rendered count, including duped models
		self.tri_index_count = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('full', Short, (0, None), (False, None), (lambda context: context.version <= 13, None))
		yield ('half', Short, (0, None), (False, None), (lambda context: context.version <= 13, None))
		yield ('lod_index', Ushort, (0, None), (False, None), (lambda context: context.version <= 13, None))
		yield ('distance', Float, (0, None), (False, None), (lambda context: context.version >= 32, None))
		yield ('stream_index', Ushort, (0, None), (False, None), (lambda context: context.version >= 32, None))
		yield ('bone_index', Ushort, (0, None), (False, None), (None, None))
		yield ('first_object_index', Ushort, (0, None), (False, None), (None, None))
		yield ('first_object_index_1', Ushort, (0, None), (False, None), (lambda context: context.version <= 13, None))
		yield ('first_object_index_2', Ushort, (0, None), (False, None), (lambda context: context.version <= 13, None))
		yield ('last_object_index', Ushort, (0, None), (False, None), (None, None))
		yield ('vertex_count', Uint, (0, None), (False, None), (lambda context: context.version >= 32 and not (((context.version == 51) or (context.version == 52)) and context.biosyn), None))
		yield ('tri_index_count', Uint, (0, None), (False, None), (lambda context: context.version >= 32 and not (((context.version == 51) or (context.version == 52)) and context.biosyn), None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 13:
			yield 'full', Short, (0, None), (False, None)
			yield 'half', Short, (0, None), (False, None)
			yield 'lod_index', Ushort, (0, None), (False, None)
		if instance.context.version >= 32:
			yield 'distance', Float, (0, None), (False, None)
			yield 'stream_index', Ushort, (0, None), (False, None)
		yield 'bone_index', Ushort, (0, None), (False, None)
		yield 'first_object_index', Ushort, (0, None), (False, None)
		if instance.context.version <= 13:
			yield 'first_object_index_1', Ushort, (0, None), (False, None)
			yield 'first_object_index_2', Ushort, (0, None), (False, None)
		yield 'last_object_index', Ushort, (0, None), (False, None)
		if instance.context.version >= 32 and not (((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn):
			yield 'vertex_count', Uint, (0, None), (False, None)
			yield 'tri_index_count', Uint, (0, None), (False, None)


LodInfo.init_attributes()
