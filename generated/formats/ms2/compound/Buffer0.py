import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.BufferInfoZTHeader import BufferInfoZTHeader


class Buffer0:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# djb hashes
		self.name_hashes = numpy.zeros((), dtype='uint')

		# names
		self.names = Array(self.context)

		# align to 4
		self.names_padding = numpy.zeros(((4 - (self.names.io_size % 4)) % 4), dtype='ubyte')
		self.zt_streams_header = BufferInfoZTHeader(self.context, self.arg, None)
		self.set_defaults()

	def set_defaults(self):
		self.name_hashes = numpy.zeros((), dtype='uint')
		self.names = Array(self.context)
		if self.context.version >= 50:
			self.names_padding = numpy.zeros(((4 - (self.names.io_size % 4)) % 4), dtype='ubyte')
		if self.context.version == 13:
			self.zt_streams_header = BufferInfoZTHeader(self.context, self.arg, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.name_hashes = stream.read_uints((self.arg.name_count))
		self.names = stream.read_zstrings((self.arg.name_count))
		if self.context.version >= 50:
			self.names_padding = stream.read_ubytes(((4 - (self.names.io_size % 4)) % 4))
		if self.context.version == 13:
			self.zt_streams_header = stream.read_type(BufferInfoZTHeader, (self.context, self.arg, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uints(self.name_hashes)
		stream.write_zstrings(self.names)
		if self.context.version >= 50:
			self.names_padding.resize(((4 - (self.names.io_size % 4)) % 4))
			stream.write_ubytes(self.names_padding)
		if self.context.version == 13:
			stream.write_type(self.zt_streams_header)

		self.io_size = stream.tell() - self.io_start

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
