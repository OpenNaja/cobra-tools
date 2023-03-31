import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compounds.MeshCollisionBit import MeshCollisionBit
from generated.formats.ms2.compounds.Vector3 import Vector3


class SubCollChunk(BaseStruct):

	__name__ = 'SubCollChunk'

	_import_key = 'ms2.compounds.SubCollChunk'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

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
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('bounds_min_repeat', Vector3, (0, None), (False, None), (None, None))
		yield ('bounds_max_repeat', Vector3, (0, None), (False, None), (None, None))
		yield ('tri_flags_count', Uint, (0, None), (False, None), (None, None))
		yield ('count_bits', Ushort, (0, None), (False, None), (None, None))
		yield ('stuff', Array, (0, None, (9,), Ushort), (False, None), (None, None))
		yield ('collision_bits', Array, (0, None, (None,), MeshCollisionBit), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bounds_min_repeat', Vector3, (0, None), (False, None)
		yield 'bounds_max_repeat', Vector3, (0, None), (False, None)
		yield 'tri_flags_count', Uint, (0, None), (False, None)
		yield 'count_bits', Ushort, (0, None), (False, None)
		yield 'stuff', Array, (0, None, (9,), Ushort), (False, None)
		yield 'collision_bits', Array, (0, None, (instance.count_bits,), MeshCollisionBit), (False, None)


SubCollChunk.init_attributes()
