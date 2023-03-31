from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RenderFeatureItem(MemStruct):

	__name__ = 'RenderFeatureItem'

	_import_key = 'renderfeaturecollection.compounds.RenderFeatureItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.item_data_count = 0
		self.item_name = Pointer(self.context, 0, ZString)
		self.item_data = ArrayPointer(self.context, self.item_data_count, RenderFeatureItem._import_map["renderfeaturecollection.compounds.RenderFeatureSubItem"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('item_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('item_data', ArrayPointer, (None, RenderFeatureItem._import_map["renderfeaturecollection.compounds.RenderFeatureSubItem"]), (False, None), (None, None))
		yield ('item_data_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item_name', Pointer, (0, ZString), (False, None)
		yield 'item_data', ArrayPointer, (instance.item_data_count, RenderFeatureItem._import_map["renderfeaturecollection.compounds.RenderFeatureSubItem"]), (False, None)
		yield 'item_data_count', Uint64, (0, None), (False, None)


RenderFeatureItem.init_attributes()
