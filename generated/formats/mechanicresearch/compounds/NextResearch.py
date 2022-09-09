from generated.array import Array
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class NextResearch(MemStruct):

	__name__ = 'NextResearch'

	_import_key = 'mechanicresearch.compounds.NextResearch'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_1 = 0
		self.item_name = Array(self.context, 0, ZString, (0,), Pointer)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item_name', Array, (0, ZString, (instance.arg,), Pointer), (False, None)
		yield 'unk_1', Uint64, (0, None), (False, None)
