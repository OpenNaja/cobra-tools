from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Sixtyfour(MemStruct):

	"""
	64 bytes
	"""

	__name__ = 'Sixtyfour'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = name_type_map['Uint64'](self.context, 0, None)
		self.count_1 = name_type_map['Uint64'](self.context, 0, None)
		self.count_2 = name_type_map['Uint64'](self.context, 0, None)
		self.count_3 = name_type_map['Uint64'](self.context, 0, None)
		self.ptr_0 = name_type_map['Pointer'](self.context, 0, None)
		self.ptr_1 = name_type_map['Pointer'](self.context, 0, None)
		self.ptr_2 = name_type_map['Pointer'](self.context, 0, None)
		self.ptr_3 = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'count_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'count_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ptr_2', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'ptr_3', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'count_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, None), (False, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, None), (False, None)
		yield 'count_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ptr_2', name_type_map['Pointer'], (0, None), (False, None)
		yield 'ptr_3', name_type_map['Pointer'], (0, None), (False, None)
		yield 'count_3', name_type_map['Uint64'], (0, None), (False, None)
