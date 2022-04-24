from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.bnk.compound.AkMediaInformation import AkMediaInformation


class AkBankSourceData:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ul_plugin_i_d = 0
		self.stream_type = 0
		self.ak_media_information = AkMediaInformation(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.ul_plugin_i_d = 0
		self.stream_type = 0
		self.ak_media_information = AkMediaInformation(self.context, 0, None)

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
		instance.ul_plugin_i_d = stream.read_uint()
		instance.stream_type = stream.read_ubyte()
		instance.ak_media_information = AkMediaInformation.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.ul_plugin_i_d)
		stream.write_ubyte(instance.stream_type)
		AkMediaInformation.to_stream(stream, instance.ak_media_information)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'AkBankSourceData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* ul_plugin_i_d = {fmt_member(self.ul_plugin_i_d, indent+1)}'
		s += f'\n	* stream_type = {fmt_member(self.stream_type, indent+1)}'
		s += f'\n	* ak_media_information = {fmt_member(self.ak_media_information, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
