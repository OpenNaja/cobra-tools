from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.bnk.compounds.AkMediaInformation import AkMediaInformation


class AkBankSourceData(BaseStruct):

	__name__ = 'AkBankSourceData'

	_import_path = 'generated.formats.bnk.compounds.AkBankSourceData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ul_plugin_i_d = 0
		self.stream_type = 0
		self.ak_media_information = AkMediaInformation(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ul_plugin_i_d', Uint, (0, None), (False, None)
		yield 'stream_type', Ubyte, (0, None), (False, None)
		yield 'ak_media_information', AkMediaInformation, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AkBankSourceData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
