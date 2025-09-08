from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class NodeInitialParams(BaseStruct):

	__name__ = 'NodeInitialParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ak_prop_bundle_1 = name_type_map['AkPropBundle'](self.context, 0, None)
		self.ak_prop_bundle_2 = name_type_map['AkPropBundle'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ak_prop_bundle_1', name_type_map['AkPropBundle'], (0, None), (False, None), (None, None)
		yield 'ak_prop_bundle_2', name_type_map['AkPropBundle'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ak_prop_bundle_1', name_type_map['AkPropBundle'], (0, None), (False, None)
		yield 'ak_prop_bundle_2', name_type_map['AkPropBundle'], (0, None), (False, None)
