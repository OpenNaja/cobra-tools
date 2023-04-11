from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ThirdFrag(MemStruct):

	"""
	72 bytes
	"""

	__name__ = 'ThirdFrag'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = name_type_map['Uint64'](self.context, 0, None)
		self.count_1 = name_type_map['Uint64'](self.context, 0, None)
		self.count_2 = name_type_map['Uint64'](self.context, 0, None)
		self.count_3 = name_type_map['Uint64'](self.context, 0, None)
		self.count_4 = name_type_map['Uint64'](self.context, 0, None)
		self.lua_method = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.ptr_1 = name_type_map['Pointer'](self.context, 0, name_type_map['TwoPtrFirst'])
		self.ptr_2 = name_type_map['Pointer'](self.context, 0, name_type_map['Sixtyfour'])
		self.member = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'lua_method', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'count_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'count_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, name_type_map['TwoPtrFirst']), (False, None), (None, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'count_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ptr_2', name_type_map['Pointer'], (0, name_type_map['Sixtyfour']), (False, None), (None, None)
		yield 'count_4', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'member', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'lua_method', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'count_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'count_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, name_type_map['TwoPtrFirst']), (False, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'count_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ptr_2', name_type_map['Pointer'], (0, name_type_map['Sixtyfour']), (False, None)
		yield 'count_4', name_type_map['Uint64'], (0, None), (False, None)
		yield 'member', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
