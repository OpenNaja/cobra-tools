import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString
from generated.formats.ms2.compound.Ms2BufferInfoZTHeader import Ms2BufferInfoZTHeader
from generated.formats.ms2.compound.SmartPadding import SmartPadding


class Ms2Buffer0:

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

		# todo - pad to 8; for pz 1.6
		self.new_padding = SmartPadding(self.context, 0, None)
		self.zt_streams_header = Ms2BufferInfoZTHeader(self.context, self.arg, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.name_hashes = numpy.zeros((self.arg.name_count,), dtype=numpy.dtype('uint32'))
		self.names = Array((self.arg.name_count,), ZString, self.context, 0, None)
		if ((not self.context.user_version.is_jwe) and (self.context.version == 20)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.new_padding = SmartPadding(self.context, 0, None)
		if self.context.version == 17:
			self.zt_streams_header = Ms2BufferInfoZTHeader(self.context, self.arg, None)

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
		if ((not instance.context.user_version.is_jwe) and (instance.context.version == 20)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			instance.new_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 17:
			instance.zt_streams_header = Ms2BufferInfoZTHeader.from_stream(stream, instance.context, instance.arg, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uints(instance.name_hashes)
		stream.write_zstrings(instance.names)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version == 20)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			SmartPadding.to_stream(stream, instance.new_padding)
		if instance.context.version == 17:
			Ms2BufferInfoZTHeader.to_stream(stream, instance.zt_streams_header)

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
