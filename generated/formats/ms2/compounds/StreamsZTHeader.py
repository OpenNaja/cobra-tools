from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.compounds.InfoZTMemPool import InfoZTMemPool
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class StreamsZTHeader(BaseStruct):

	"""
	266 bytes ?
	very end of buffer 0 after the names list
	"""

	__name__ = 'StreamsZTHeader'

	_import_path = 'generated.formats.ms2.compounds.StreamsZTHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# sometimes 00 byte
		self.weird_padding = SmartPadding(self.context, 0, None)

		# ?
		self.unks = Array(self.context, 0, None, (0,), InfoZTMemPool)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.weird_padding = SmartPadding(self.context, 0, None)
		self.unks = Array(self.context, 0, None, (self.arg.stream_count,), InfoZTMemPool)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.weird_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.unks = Array.from_stream(stream, instance.context, 0, None, (instance.arg.stream_count,), InfoZTMemPool)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		SmartPadding.to_stream(stream, instance.weird_padding)
		Array.to_stream(stream, instance.unks, instance.context, 0, None, (instance.arg.stream_count,), InfoZTMemPool)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'weird_padding', SmartPadding, (0, None), (False, None)
		yield 'unks', Array, (0, None, (instance.arg.stream_count,), InfoZTMemPool), (False, None)

	def get_info_str(self, indent=0):
		return f'StreamsZTHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* weird_padding = {self.fmt_member(self.weird_padding, indent+1)}'
		s += f'\n	* unks = {self.fmt_member(self.unks, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
