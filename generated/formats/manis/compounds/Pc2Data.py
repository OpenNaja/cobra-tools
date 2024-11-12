from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class Pc2Data(BaseStruct):

	"""
	in seemingly uncompressed manis
	"""

	__name__ = 'PC2Data'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.z_0 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.c_0 = name_type_map['Uint64'](self.context, 0, None)
		self.z_1 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.c_2 = name_type_map['Uint64'](self.context, 0, None)
		self.z_2 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.c_3 = name_type_map['Uint64'](self.context, 0, None)
		self.z_3 = name_type_map['Uint64'](self.context, 0, None)
		self.following_size = name_type_map['Ushort'](self.context, 0, None)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.databytes = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.ref_2 = name_type_map['Empty'](self.context, 0, None)
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
		yield 'c_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'z_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'following_size', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'databytes', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'z_0', Array, (0, None, (3,), name_type_map['Uint64']), (False, None)
		yield 'c_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'z_1', Array, (0, None, (3,), name_type_map['Uint64']), (False, None)
		yield 'c_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'z_2', Array, (0, None, (7,), name_type_map['Uint64']), (False, None)
		yield 'c_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'z_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'following_size', name_type_map['Ushort'], (0, None), (False, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'databytes', Array, (0, None, (instance.following_size,), name_type_map['Ubyte']), (False, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None)
