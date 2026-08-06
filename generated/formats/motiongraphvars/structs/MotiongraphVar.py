from generated.formats.motiongraphvars.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MotiongraphVar(MemStruct):

	"""
	PZ, JWE3: 48 bytes
	"""

	__name__ = 'MotiongraphVar'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = name_type_map['Uint64'](self.context, 0, None)
		self.b_0 = name_type_map['Float'](self.context, 0, None)
		self.b_1 = name_type_map['Float'](self.context, 0, None)
		self.ten = name_type_map['Uint64'].from_value(10)
		self.d = name_type_map['Uint64'](self.context, 0, None)
		self.e = name_type_map['Uint64'](self.context, 0, None)
		self.var_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'var_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'a', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'b_0', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'b_1', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'ten', name_type_map['Uint64'], (0, None), (False, 10), (None, None)
		yield 'd', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'e', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'var_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'a', name_type_map['Uint64'], (0, None), (False, None)
		yield 'b_0', name_type_map['Float'], (0, None), (False, None)
		yield 'b_1', name_type_map['Float'], (0, None), (False, None)
		yield 'ten', name_type_map['Uint64'], (0, None), (False, 10)
		yield 'd', name_type_map['Uint64'], (0, None), (False, None)
		yield 'e', name_type_map['Uint64'], (0, None), (False, None)
