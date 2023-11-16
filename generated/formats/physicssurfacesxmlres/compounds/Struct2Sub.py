from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class Struct2Sub(MemStruct):

	"""
	PC: 72 bytes
	"""

	__name__ = 'Struct2Sub'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = name_type_map['Float'](self.context, 0, None)
		self.float_2 = name_type_map['Float'](self.context, 0, None)
		self.float_3 = name_type_map['Float'](self.context, 0, None)
		self.float_4 = name_type_map['Float'](self.context, 0, None)
		self.c = name_type_map['Uint64'](self.context, 0, None)
		self.d = name_type_map['Uint64'](self.context, 0, None)
		self.e = name_type_map['Uint64'](self.context, 0, None)
		self.f = name_type_map['Uint64'](self.context, 0, None)
		self.count_0 = name_type_map['Uint'](self.context, 0, None)
		self.count_1 = name_type_map['Uint'](self.context, 0, None)
		self.name_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.nil = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'float_1', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_4', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'c', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'd', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'e', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'f', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'nil', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'count_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'count_1', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, None)
		yield 'float_4', name_type_map['Float'], (0, None), (False, None)
		yield 'c', name_type_map['Uint64'], (0, None), (False, None)
		yield 'd', name_type_map['Uint64'], (0, None), (False, None)
		yield 'e', name_type_map['Uint64'], (0, None), (False, None)
		yield 'f', name_type_map['Uint64'], (0, None), (False, None)
		yield 'nil', name_type_map['Pointer'], (0, None), (False, None)
		yield 'count_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'count_1', name_type_map['Uint'], (0, None), (False, None)
