from generated.formats.janitorsettings.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class JanitorBetweenArrays(MemStruct):

	"""
	# only in PZ
	"""

	__name__ = 'JanitorBetweenArrays'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = name_type_map['Float'].from_value(1.0)
		self.b = name_type_map['Float'].from_value(0.5)
		self.c = name_type_map['Uint64'].from_value(0)
		self.d = name_type_map['Float'].from_value(0.2)
		self.e = name_type_map['Float'].from_value(1.0)
		self.f = name_type_map['Float'].from_value(1.0)
		self.g = name_type_map['Float'].from_value(1.0)
		self.h = name_type_map['Float'].from_value(0.0)
		self.i = name_type_map['Float'].from_value(1.0)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', name_type_map['Float'], (0, None), (False, 1.0), (None, None)
		yield 'b', name_type_map['Float'], (0, None), (False, 0.5), (None, None)
		yield 'c', name_type_map['Uint64'], (0, None), (False, 0), (None, None)
		yield 'd', name_type_map['Float'], (0, None), (False, 0.2), (None, None)
		yield 'e', name_type_map['Float'], (0, None), (False, 1.0), (None, None)
		yield 'f', name_type_map['Float'], (0, None), (False, 1.0), (None, None)
		yield 'g', name_type_map['Float'], (0, None), (False, 1.0), (None, None)
		yield 'h', name_type_map['Float'], (0, None), (False, 0.0), (None, None)
		yield 'i', name_type_map['Float'], (0, None), (False, 1.0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', name_type_map['Float'], (0, None), (False, 1.0)
		yield 'b', name_type_map['Float'], (0, None), (False, 0.5)
		yield 'c', name_type_map['Uint64'], (0, None), (False, 0)
		yield 'd', name_type_map['Float'], (0, None), (False, 0.2)
		yield 'e', name_type_map['Float'], (0, None), (False, 1.0)
		yield 'f', name_type_map['Float'], (0, None), (False, 1.0)
		yield 'g', name_type_map['Float'], (0, None), (False, 1.0)
		yield 'h', name_type_map['Float'], (0, None), (False, 0.0)
		yield 'i', name_type_map['Float'], (0, None), (False, 1.0)
