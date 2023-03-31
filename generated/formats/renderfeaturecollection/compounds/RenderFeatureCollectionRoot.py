from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RenderFeatureCollectionRoot(MemStruct):

	__name__ = 'RenderFeatureCollectionRoot'

	_import_key = 'renderfeaturecollection.compounds.RenderFeatureCollectionRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.item_count = 0
		self.item_list = ArrayPointer(self.context, self.item_count, RenderFeatureCollectionRoot._import_map["renderfeaturecollection.compounds.RenderFeatureItem"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('item_list', ArrayPointer, (None, RenderFeatureCollectionRoot._import_map["renderfeaturecollection.compounds.RenderFeatureItem"]), (False, None), (None, None))
		yield ('item_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item_list', ArrayPointer, (instance.item_count, RenderFeatureCollectionRoot._import_map["renderfeaturecollection.compounds.RenderFeatureItem"]), (False, None)
		yield 'item_count', Uint64, (0, None), (False, None)


RenderFeatureCollectionRoot.init_attributes()
