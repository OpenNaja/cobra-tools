import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString
from generated.formats.ms2.compound.Ms2BufferInfoZTHeader import Ms2BufferInfoZTHeader
from generated.formats.ms2.compound.SmartPadding import SmartPadding


class Ms2Buffer0:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# djb hashes
		self.name_hashes = numpy.zeros((self.arg.name_count), dtype=numpy.dtype('uint32'))

		# names
		self.names = Array((self.arg.name_count), ZString, self.context, None, None)

		# todo - pad to 8; for pz 1.6
		self.new_padding = SmartPadding(self.context, None, None)
		self.zt_streams_header = Ms2BufferInfoZTHeader(self.context, self.arg, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.name_hashes = numpy.zeros((self.arg.name_count), dtype=numpy.dtype('uint32'))
		self.names = Array((self.arg.name_count), ZString, self.context, None, None)
		if ((not self.context.user_version.is_jwe) and (self.context.version == 20)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.new_padding = SmartPadding(self.context, None, None)
		if self.context.version == 17:
			self.zt_streams_header = Ms2BufferInfoZTHeader(self.context, self.arg, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.name_hashes = stream.read_uints((self.arg.name_count))
		self.names = stream.read_zstrings((self.arg.name_count))
		if ((not self.context.user_version.is_jwe) and (self.context.version == 20)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.new_padding = stream.read_type(SmartPadding, (self.context, None, None))
		if self.context.version == 17:
			self.zt_streams_header = stream.read_type(Ms2BufferInfoZTHeader, (self.context, self.arg, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uints(self.name_hashes)
		stream.write_zstrings(self.names)
		if ((not self.context.user_version.is_jwe) and (self.context.version == 20)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			stream.write_type(self.new_padding)
		if self.context.version == 17:
			stream.write_type(self.zt_streams_header)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2Buffer0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_hashes = {self.name_hashes.__repr__()}'
		s += f'\n	* names = {self.names.__repr__()}'
		s += f'\n	* new_padding = {self.new_padding.__repr__()}'
		s += f'\n	* zt_streams_header = {self.zt_streams_header.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
