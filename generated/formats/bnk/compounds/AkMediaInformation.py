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
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.source_i_d = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_in_memory_media_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_source_bits = Ubyte.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.source_i_d)
		Uint.to_stream(stream, instance.u_in_memory_media_size)
		Ubyte.to_stream(stream, instance.u_source_bits)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'source_i_d', Uint, (0, None), (False, None)
		yield 'u_in_memory_media_size', Uint, (0, None), (False, None)
		yield 'u_source_bits', Ubyte, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AkMediaInformation [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* source_i_d = {self.fmt_member(self.source_i_d, indent+1)}'
		s += f'\n	* u_in_memory_media_size = {self.fmt_member(self.u_in_memory_media_size, indent+1)}'
		s += f'\n	* u_source_bits = {self.fmt_member(self.u_source_bits, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
