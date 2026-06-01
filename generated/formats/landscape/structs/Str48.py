from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class Str48(BaseStruct):

	"""
	48 bytes
	"""

	__name__ = 'Str48'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.quat = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.v_1 = name_type_map['Vector3'](self.context, 0, None)
		self.v_2 = name_type_map['Vector3'](self.context, 0, None)
		self.a = name_type_map['Ushort'](self.context, 0, None)
		self.b = name_type_map['Ushort'](self.context, 0, None)
		self.index = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'quat', Array, (0, None, (4,), name_type_map['Float']), (False, None), (None, None)
		yield 'v_1', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'v_2', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'index', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'quat', Array, (0, None, (4,), name_type_map['Float']), (False, None)
		yield 'v_1', name_type_map['Vector3'], (0, None), (False, None)
		yield 'v_2', name_type_map['Vector3'], (0, None), (False, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None)
		yield 'index', name_type_map['Uint'], (0, None), (False, None)
