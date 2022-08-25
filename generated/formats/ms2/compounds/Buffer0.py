import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ms2.compounds.StreamsZTHeader import StreamsZTHeader


class Buffer0(BaseStruct):

	__name__ = 'Buffer0'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# djb2 hashes
		self.name_hashes = Array((0,), Uint, self.context, 0, None)

		# names
		self.names = Array((0,), ZString, self.context, 0, None)

		# align to 4
		self.names_padding = Array((0,), Ubyte, self.context, 0, None)
		self.zt_streams_header = StreamsZTHeader(self.context, self.arg, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.name_hashes = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint32'))
		self.names = Array((self.arg.name_count,), ZString, self.context, 0, None)
		if self.context.version >= 50:
			self.names_padding = numpy.zeros(((4 - (self.names.io_size % 4)) % 4,), dtype=numpy.dtype('uint8'))
		if self.context.version <= 13:
			self.zt_streams_header = StreamsZTHeader(self.context, self.arg, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.name_hashes = Array.from_stream(stream, instance.context, 0, None, (instance.arg.name_count,), Uint)
		instance.names = Array.from_stream(stream, instance.context, 0, None, (instance.arg.name_count,), ZString)
		if instance.context.version >= 50:
			instance.names_padding = Array.from_stream(stream, instance.context, 0, None, ((4 - (instance.names.io_size % 4)) % 4,), Ubyte)
		if instance.context.version <= 13:
			instance.zt_streams_header = StreamsZTHeader.from_stream(stream, instance.context, instance.arg, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.name_hashes, (instance.arg.name_count,), Uint, instance.context, 0, None)
		Array.to_stream(stream, instance.names, (instance.arg.name_count,), ZString, instance.context, 0, None)
		if instance.context.version >= 50:
			instance.names_padding.resize(((4 - (instance.names.io_size % 4)) % 4,))
			Array.to_stream(stream, instance.names_padding, ((4 - (instance.names.io_size % 4)) % 4,), Ubyte, instance.context, 0, None)
		if instance.context.version <= 13:
			StreamsZTHeader.to_stream(stream, instance.zt_streams_header)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'name_hashes', Array, ((instance.arg.name_count,), Uint, 0, None), (False, None)
		yield 'names', Array, ((instance.arg.name_count,), ZString, 0, None), (False, None)
		if instance.context.version >= 50:
			yield 'names_padding', Array, (((4 - (instance.names.io_size % 4)) % 4,), Ubyte, 0, None), (False, None)
		if instance.context.version <= 13:
			yield 'zt_streams_header', StreamsZTHeader, (instance.arg, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Buffer0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* name_hashes = {self.fmt_member(self.name_hashes, indent+1)}'
		s += f'\n	* names = {self.fmt_member(self.names, indent+1)}'
		s += f'\n	* names_padding = {self.fmt_member(self.names_padding, indent+1)}'
		s += f'\n	* zt_streams_header = {self.fmt_member(self.zt_streams_header, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
