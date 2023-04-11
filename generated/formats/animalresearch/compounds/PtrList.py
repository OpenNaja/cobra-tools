from generated.array import Array
from generated.formats.animalresearch.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PtrList(MemStruct):

	__name__ = 'PtrList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, name_type_map['ZString'], (0,), name_type_map['Pointer'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ptrs', Array, (0, name_type_map['ZString'], (None,), name_type_map['Pointer']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptrs', Array, (0, name_type_map['ZString'], (instance.arg,), name_type_map['Pointer']), (False, None)
