from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint


class AkMediaInformation(BaseStruct):

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

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.source_i_d = stream.read_uint()
		instance.u_in_memory_media_size = stream.read_uint()
		instance.u_source_bits = stream.read_ubyte()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.source_i_d)
		stream.write_uint(instance.u_in_memory_media_size)
		stream.write_ubyte(instance.u_source_bits)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'source_i_d', Uint, (0, None)
		yield 'u_in_memory_media_size', Uint, (0, None)
		yield 'u_source_bits', Ubyte, (0, None)

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
