from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString
from generated.formats.ms2.compound.StreamsZTHeader import StreamsZTHeader


class Buffer0:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# djb2 hashes
		self.name_hashes = 0

		# names
		self.names = 0

		# align to 4
		self.names_padding = 0
		self.zt_streams_header = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.name_hashes = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint32'))
		self.names = Array((self.arg.name_count,), ZString, self.context, 0, None)
		if self.context.version >= 50:
			self.names_padding = numpy.zeros(((4 - (self.names.io_size % 4)) % 4,), dtype=numpy.dtype('uint8'))
		if self.context.version <= 13:
			self.zt_streams_header = StreamsZTHeader(self.context, self.arg, None)

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
		instance.name_hashes = stream.read_uints((instance.arg.name_count,))
		instance.names = stream.read_zstrings((instance.arg.name_count,))
		if instance.context.version >= 50:
			instance.names_padding = stream.read_ubytes(((4 - (instance.names.io_size % 4)) % 4,))
		if instance.context.version <= 13:
			instance.zt_streams_header = StreamsZTHeader.from_stream(stream, instance.context, instance.arg, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uints(instance.name_hashes)
		stream.write_zstrings(instance.names)
		if instance.context.version >= 50:
			instance.names_padding.resize(((4 - (instance.names.io_size % 4)) % 4,))
			stream.write_ubytes(instance.names_padding)
		if instance.context.version <= 13:
			StreamsZTHeader.to_stream(stream, instance.zt_streams_header)

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
		return f'Buffer0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* name_hashes = {fmt_member(self.name_hashes, indent+1)}'
		s += f'\n	* names = {fmt_member(self.names, indent+1)}'
		s += f'\n	* names_padding = {fmt_member(self.names_padding, indent+1)}'
		s += f'\n	* zt_streams_header = {fmt_member(self.zt_streams_header, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
