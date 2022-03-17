import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString
from generated.formats.ms2.compound.BufferInfoZTHeader import BufferInfoZTHeader


class Buffer0:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# djb hashes
		self.name_hashes = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint32'))

		# names
		self.names = Array((self.arg.name_count,), ZString, self.context, 0, None)

		# align to 4
		self.names_padding = numpy.zeros(((4 - (self.names.io_size % 4)) % 4,), dtype=numpy.dtype('uint8'))
		self.zt_streams_header = BufferInfoZTHeader(self.context, self.arg, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.name_hashes = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint32'))
		self.names = Array((self.arg.name_count,), ZString, self.context, 0, None)
		if self.context.version >= 50:
			self.names_padding = numpy.zeros(((4 - (self.names.io_size % 4)) % 4,), dtype=numpy.dtype('uint8'))
		if self.context.version == 13:
			self.zt_streams_header = BufferInfoZTHeader(self.context, self.arg, None)

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
		if instance.context.version == 13:
			instance.zt_streams_header = BufferInfoZTHeader.from_stream(stream, instance.context, instance.arg, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uints(instance.name_hashes)
		stream.write_zstrings(instance.names)
		if instance.context.version >= 50:
			instance.names_padding.resize(((4 - (instance.names.io_size % 4)) % 4,))
			stream.write_ubytes(instance.names_padding)
		if instance.context.version == 13:
			BufferInfoZTHeader.to_stream(stream, instance.zt_streams_header)

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

	def get_info_str(self):
		return f'Buffer0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_hashes = {self.name_hashes.__repr__()}'
		s += f'\n	* names = {self.names.__repr__()}'
		s += f'\n	* names_padding = {self.names_padding.__repr__()}'
		s += f'\n	* zt_streams_header = {self.zt_streams_header.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
