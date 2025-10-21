from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class MeshCollisionChunk(BaseStruct):

	__name__ = 'MeshCollisionChunk'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.a = Array(self.context, 0, None, (0,), name_type_map['Short'])

		# start indices of a group of 16 tris;incrementing by 16 from 0, or if around -32769: incrementing by 1, mostly
		self.tri_indices = Array(self.context, 0, None, (0,), name_type_map['Short'])

		# usually, but not always the first tri index; 0 if tri_indices are negative
		self.min_of_indices = name_type_map['Short'](self.context, 0, None)

		# counts how many slots in tri_indices are used, others are 0
		self.num_used_tri_slots = name_type_map['Ubyte'](self.context, 0, None)

		# likely
		self.salt_index = name_type_map['Ubyte'](self.context, 0, None)

		# always 2954754766?
		self.consts = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', Array, (0, None, (24,), name_type_map['Short']), (False, None), (None, None)
		yield 'tri_indices', Array, (0, None, (8,), name_type_map['Short']), (False, None), (None, None)
		yield 'min_of_indices', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'num_used_tri_slots', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'salt_index', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'consts', Array, (0, None, (3,), name_type_map['Uint']), (False, 2954754766), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Array, (0, None, (24,), name_type_map['Short']), (False, None)
		yield 'tri_indices', Array, (0, None, (8,), name_type_map['Short']), (False, None)
		yield 'min_of_indices', name_type_map['Short'], (0, None), (False, None)
		yield 'num_used_tri_slots', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'salt_index', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'consts', Array, (0, None, (3,), name_type_map['Uint']), (False, 2954754766)
