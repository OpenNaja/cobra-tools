from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PtrList(MemStruct):

	__name__ = 'PtrList'

	_import_key = 'mergedetails.compounds.PtrList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, ZString, (0,), Pointer)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('ptrs', Array, (0, ZString, (None,), Pointer), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptrs', Array, (0, ZString, (instance.arg,), Pointer), (False, None)


PtrList.init_attributes()
