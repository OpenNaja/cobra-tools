from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RenderFeatureSubItem(MemStruct):

	__name__ = 'RenderFeatureSubItem'

	_import_key = 'renderfeaturecollection.compounds.RenderFeatureSubItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.sub_item_value_or_flags = 0
		self.sub_item_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('sub_item_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('sub_item_value_or_flags', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'sub_item_name', Pointer, (0, ZString), (False, None)
		yield 'sub_item_value_or_flags', Uint64, (0, None), (False, None)


RenderFeatureSubItem.init_attributes()
