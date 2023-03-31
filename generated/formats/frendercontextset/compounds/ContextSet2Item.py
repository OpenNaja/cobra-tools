from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ContextSet2Item(MemStruct):

	__name__ = 'ContextSet2Item'

	_import_key = 'frendercontextset.compounds.ContextSet2Item'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.stuff_2_id = 0
		self.stuff_2_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('stuff_2_name', Pointer, (0, ZString), (False, None), None)
		yield ('stuff_2_id', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'stuff_2_name', Pointer, (0, ZString), (False, None)
		yield 'stuff_2_id', Uint64, (0, None), (False, None)


ContextSet2Item.init_attributes()
