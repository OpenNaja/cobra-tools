from generated.formats.bnk.imports import name_type_map
from generated.formats.bnk.structs.HircObject import HircObject


class Sound(HircObject):

	__name__ = 'Sound'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ak_bank_source_data = name_type_map['AkBankSourceData'](self.context, 0, None)
		self.node_base_params = name_type_map['NodeBaseParams'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ak_bank_source_data', name_type_map['AkBankSourceData'], (0, None), (False, None), (None, None)
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ak_bank_source_data', name_type_map['AkBankSourceData'], (0, None), (False, None)
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None)
