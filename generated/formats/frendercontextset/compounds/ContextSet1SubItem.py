from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ContextSet1SubItem(MemStruct):

	__name__ = 'ContextSet1SubItem'

	_import_key = 'frendercontextset.compounds.ContextSet1SubItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.stuff_1_sub_order_or_flags = 0
		self.stuff_1_sub_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('stuff_1_sub_name', Pointer, (0, ZString), (False, None), None),
		('stuff_1_sub_order_or_flags', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'stuff_1_sub_name', Pointer, (0, ZString), (False, None)
		yield 'stuff_1_sub_order_or_flags', Uint64, (0, None), (False, None)
