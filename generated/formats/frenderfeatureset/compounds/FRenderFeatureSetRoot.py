from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FRenderFeatureSetRoot(MemStruct):

	__name__ = 'FRenderFeatureSetRoot'

	_import_key = 'frenderfeatureset.compounds.FRenderFeatureSetRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.featureset_count = 0
		self.unknown_always_1 = 0
		self.featureset_list = ArrayPointer(self.context, self.featureset_count, FRenderFeatureSetRoot._import_map["frenderfeatureset.compounds.FeatureSetItem"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('featureset_list', ArrayPointer, (None, None), (False, None), None)
		yield ('featureset_count', Uint, (0, None), (False, None), None)
		yield ('unknown_always_1', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'featureset_list', ArrayPointer, (instance.featureset_count, FRenderFeatureSetRoot._import_map["frenderfeatureset.compounds.FeatureSetItem"]), (False, None)
		yield 'featureset_count', Uint, (0, None), (False, None)
		yield 'unknown_always_1', Uint, (0, None), (False, None)


FRenderFeatureSetRoot.init_attributes()
