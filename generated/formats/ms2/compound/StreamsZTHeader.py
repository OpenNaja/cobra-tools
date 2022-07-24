from generated.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.ms2.compound.InfoZTMemPool import InfoZTMemPool
from generated.formats.ovl_base.compound.SmartPadding import SmartPadding
from generated.struct import StructBase


class StreamsZTHeader(StructBase):

	"""
	266 bytes ?
	very end of buffer 0 after the names list
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# sometimes 00 byte
		self.weird_padding = 0

		# ?
		self.unks = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.weird_padding = SmartPadding(self.context, 0, None)
		self.unks = Array((self.arg.stream_count,), InfoZTMemPool, self.context, 0, None)

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
		instance.weird_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.unks = Array.from_stream(stream, (instance.arg.stream_count,), InfoZTMemPool, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		SmartPadding.to_stream(stream, instance.weird_padding)
		Array.to_stream(stream, instance.unks, (instance.arg.stream_count,), InfoZTMemPool, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('weird_padding', SmartPadding, (0, None))
		yield ('unks', Array, ((instance.arg.stream_count,), InfoZTMemPool, 0, None))

	def get_info_str(self, indent=0):
		return f'StreamsZTHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* weird_padding = {fmt_member(self.weird_padding, indent+1)}'
		s += f'\n	* unks = {fmt_member(self.unks, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
