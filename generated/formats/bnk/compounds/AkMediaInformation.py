from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint


class AkMediaInformation(BaseStruct):

	__name__ = 'AkMediaInformation'

	_import_path = 'generated.formats.bnk.compounds.AkMediaInformation'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.source_i_d = 0
		self.u_in_memory_media_size = 0
		self.u_source_bits = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.source_i_d = 0
		self.u_in_memory_media_size = 0
		self.u_source_bits = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'source_i_d', Uint, (0, None), (False, None)
		yield 'u_in_memory_media_size', Uint, (0, None), (False, None)
		yield 'u_source_bits', Ubyte, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AkMediaInformation [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
