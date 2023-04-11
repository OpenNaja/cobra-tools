from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.specdef.imports import name_type_map


class BooleanData(MemStruct):

	"""
	8 bytes in log
	"""

	__name__ = 'BooleanData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = name_type_map['Ubyte'](self.context, 0, None)
		self.default = name_type_map['Ubyte'](self.context, 0, None)
		self.unused = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'value', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'default', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'unused', Array, (0, None, (6,), name_type_map['Ubyte']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'value', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'default', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'unused', Array, (0, None, (6,), name_type_map['Ubyte']), (False, None)
