from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class Something(BaseStruct):

	"""
	16 bytes
	"""

	__name__ = 'Something'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flo_22 = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.junk_22 = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'flo_22', Array, (0, None, (4,), name_type_map['Float']), (False, None), (None, None)
		yield 'junk_22', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'flo_22', Array, (0, None, (4,), name_type_map['Float']), (False, None)
		yield 'junk_22', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None)
