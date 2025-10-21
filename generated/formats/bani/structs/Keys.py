from generated.array import Array
from generated.formats.bani.imports import name_type_map
from generated.formats.ovl_base.structs.NestedPointers import NestedPointers


class Keys(NestedPointers):

	__name__ = 'Keys'


	@property
	def arg_1(self):
		return self.arg[0]
	@property
	def arg_2(self):
		return self.arg[1]

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = Array(self.context, 0, None, (0,), name_type_map['Bone'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data', Array, (0, None, (None, None,), name_type_map['Bone']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data', Array, (0, None, (instance.arg_1, instance.arg_2,), name_type_map['Bone']), (False, None)
