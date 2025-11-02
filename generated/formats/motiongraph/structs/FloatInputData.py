from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FloatInputData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'FloatInputData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float = name_type_map['Float'](self.context, 0, None)
		self.optional_var_and_curve_count = name_type_map['Uint'](self.context, 0, None)
		self.optional_var_and_curve = name_type_map['ArrayPointer'](self.context, self.optional_var_and_curve_count, name_type_map['OptionalVarAndCurve'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'float', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'optional_var_and_curve_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'optional_var_and_curve', name_type_map['ArrayPointer'], (None, name_type_map['OptionalVarAndCurve']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'float', name_type_map['Float'], (0, None), (False, None)
		yield 'optional_var_and_curve_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'optional_var_and_curve', name_type_map['ArrayPointer'], (instance.optional_var_and_curve_count, name_type_map['OptionalVarAndCurve']), (False, None)
