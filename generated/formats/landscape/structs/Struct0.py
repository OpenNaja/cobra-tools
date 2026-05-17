from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class Struct0(BaseStruct):

	__name__ = 'Struct0'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vec = name_type_map['Vector3'](self.context, 0, None)
		self.unk = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'vec', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'unk', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'vec', name_type_map['Vector3'], (0, None), (False, None)
		yield 'unk', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None)
