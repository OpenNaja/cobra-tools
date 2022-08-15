from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.bnk.compounds.AkMediaInformation import AkMediaInformation


class AkBankSourceData(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ul_plugin_i_d = 0
		self.stream_type = 0
		self.ak_media_information = AkMediaInformation(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ul_plugin_i_d = 0
		self.stream_type = 0
		self.ak_media_information = AkMediaInformation(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ul_plugin_i_d = Uint.from_stream(stream, instance.context, 0, None)
		instance.stream_type = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.ak_media_information = AkMediaInformation.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.ul_plugin_i_d)
		stream.write_ubyte(instance.stream_type)
		AkMediaInformation.to_stream(stream, instance.ak_media_information)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ul_plugin_i_d', Uint, (0, None)
		yield 'stream_type', Ubyte, (0, None)
		yield 'ak_media_information', AkMediaInformation, (0, None)

	def get_info_str(self, indent=0):
		return f'AkBankSourceData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ul_plugin_i_d = {self.fmt_member(self.ul_plugin_i_d, indent+1)}'
		s += f'\n	* stream_type = {self.fmt_member(self.stream_type, indent+1)}'
		s += f'\n	* ak_media_information = {self.fmt_member(self.ak_media_information, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
