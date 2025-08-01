from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class UncompressedManiDataPC2(BaseStruct):

	"""
	in compressed manis
	"""

	__name__ = 'UncompressedManiDataPC2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.z_0 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.c_0 = name_type_map['Uint64'](self.context, 0, None)
		self.z_1 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.c_2 = name_type_map['Uint64'](self.context, 0, None)
		self.z_2 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.target_bone_count = name_type_map['Uint64'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'z_0', Array, (0, None, (3,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'c_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'z_1', Array, (0, None, (3,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'c_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'z_2', Array, (0, None, (7,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'target_bone_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'z_0', Array, (0, None, (3,), name_type_map['Uint64']), (False, None)
		yield 'c_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'z_1', Array, (0, None, (3,), name_type_map['Uint64']), (False, None)
		yield 'c_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'z_2', Array, (0, None, (7,), name_type_map['Uint64']), (False, None)
		yield 'target_bone_count', name_type_map['Uint64'], (0, None), (False, None)
