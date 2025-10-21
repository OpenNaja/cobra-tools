from generated.array import Array
from generated.formats.ovl_base.structs.NestedPointers import NestedPointers
from generated.formats.renderparameters.imports import name_type_map


class CurveList(NestedPointers):

	__name__ = 'CurveList'


	@property
	def arg_1(self):
		return self.arg[0]
	@property
	def arg_2(self):
		return self.arg[1]

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, self.arg_2, name_type_map['KeyPoint'], (0,), name_type_map['Pointer'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ptrs', Array, (None, name_type_map['KeyPoint'], (None,), name_type_map['Pointer']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptrs', Array, (instance.arg_2, name_type_map['KeyPoint'], (instance.arg_1,), name_type_map['Pointer']), (False, None)
