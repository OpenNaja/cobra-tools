from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class MeshCollisionOptimizer(BaseStruct):

	__name__ = 'MeshCollisionOptimizer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# verbatim
		self.bounds_min_repeat = name_type_map['Vector3'](self.context, 0, None)

		# verbatim
		self.bounds_max_repeat = name_type_map['Vector3'](self.context, 0, None)

		# seems to repeat tri_count
		self.tri_flags_count = name_type_map['Uint'](self.context, 0, None)
		self.chunks_count = name_type_map['Ushort'](self.context, 0, None)

		# seen 272 in JWE2
		self.some_index = name_type_map['Ushort'](self.context, 0, None)

		# seen 0 in JWE2
		self.zeros = Array(self.context, 0, None, (0,), name_type_map['Ushort'])
		self.chunks = Array(self.context, 0, None, (0,), name_type_map['MeshCollisionChunk'])

		# usually zero, nonzero in JWE2 dev footplant, [1] used as salt for tri indices
		self.tris_salt = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'bounds_min_repeat', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'bounds_max_repeat', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'tri_flags_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'chunks_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'some_index', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zeros', Array, (0, None, (8,), name_type_map['Ushort']), (False, None), (None, None)
		yield 'chunks', Array, (0, None, (None,), name_type_map['MeshCollisionChunk']), (False, None), (None, None)
		yield 'tris_salt', Array, (0, None, (4,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bounds_min_repeat', name_type_map['Vector3'], (0, None), (False, None)
		yield 'bounds_max_repeat', name_type_map['Vector3'], (0, None), (False, None)
		yield 'tri_flags_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'chunks_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'some_index', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zeros', Array, (0, None, (8,), name_type_map['Ushort']), (False, None)
		yield 'chunks', Array, (0, None, (instance.chunks_count,), name_type_map['MeshCollisionChunk']), (False, None)
		yield 'tris_salt', Array, (0, None, (4,), name_type_map['Uint']), (False, None)
