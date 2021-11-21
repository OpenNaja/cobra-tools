import numpy
from generated.array import Array
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader
from generated.formats.tex.compound.Frag00 import Frag00
from generated.formats.tex.compound.Header3Data0 import Header3Data0
from generated.formats.tex.compound.Header7Data1 import Header7Data1
from generated.formats.tex.compound.TexBuffer import TexBuffer
from generated.formats.tex.compound.TexBufferPc import TexBufferPc
from generated.formats.tex.compound.TexHeader import TexHeader


class TexInfoHeader(GenericHeader):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.tex_info = TexHeader(self.context, 0, None)
		self.frag_00 = Frag00(self.context, 0, None)
		self.frag_10 = Header3Data0(self.context, 0, None)
		self.frag_01 = Array((self.frag_10.stream_count,), TexBuffer, self.context, 0, None)
		self.frag_01 = Array((self.frag_10.stream_count,), TexBufferPc, self.context, 0, None)
		self.frag_11 = Header7Data1(self.context, 0, None)

		# pad whole frag_11 struct to 320 bytes
		self.padding = numpy.zeros((320 - self.frag_11.io_size,), dtype=numpy.dtype('uint8'))

		# pad whole frag_11 struct to 320 bytes
		self.padding = numpy.zeros((384 - self.frag_11.io_size,), dtype=numpy.dtype('uint8'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.tex_info = TexHeader(self.context, 0, None)
		if not (self.context.version < 19):
			self.frag_00 = Frag00(self.context, 0, None)
		self.frag_10 = Header3Data0(self.context, 0, None)
		if not (self.context.version < 19):
			self.frag_01 = Array((self.frag_10.stream_count,), TexBuffer, self.context, 0, None)
		if self.context.version < 19:
			self.frag_01 = Array((self.frag_10.stream_count,), TexBufferPc, self.context, 0, None)
		if not (self.context.version < 19):
			self.frag_11 = Header7Data1(self.context, 0, None)
		if ((not self.context.user_version.is_jwe) and (self.context.version == 20)) or (((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20))):
			self.padding = numpy.zeros((320 - self.frag_11.io_size,), dtype=numpy.dtype('uint8'))
		if self.context.user_version.is_jwe and (self.context.version == 19):
			self.padding = numpy.zeros((384 - self.frag_11.io_size,), dtype=numpy.dtype('uint8'))

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
		instance.tex_info = TexHeader.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version < 19):
			instance.frag_00 = Frag00.from_stream(stream, instance.context, 0, None)
		instance.frag_10 = Header3Data0.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version < 19):
			instance.frag_01 = Array.from_stream(stream, (instance.frag_10.stream_count,), TexBuffer, instance.context, 0, None)
		if instance.context.version < 19:
			instance.frag_01 = Array.from_stream(stream, (instance.frag_10.stream_count,), TexBufferPc, instance.context, 0, None)
		if not (instance.context.version < 19):
			instance.frag_11 = Header7Data1.from_stream(stream, instance.context, 0, None)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version == 20)) or (((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20))):
			instance.padding = stream.read_ubytes((320 - instance.frag_11.io_size,))
		if instance.context.user_version.is_jwe and (instance.context.version == 19):
			instance.padding = stream.read_ubytes((384 - instance.frag_11.io_size,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		TexHeader.to_stream(stream, instance.tex_info)
		if not (instance.context.version < 19):
			Frag00.to_stream(stream, instance.frag_00)
		Header3Data0.to_stream(stream, instance.frag_10)
		if not (instance.context.version < 19):
			Array.to_stream(stream, instance.frag_01, (instance.frag_10.stream_count,),TexBuffer, instance.context, 0, None)
		if instance.context.version < 19:
			Array.to_stream(stream, instance.frag_01, (instance.frag_10.stream_count,),TexBufferPc, instance.context, 0, None)
		if not (instance.context.version < 19):
			Header7Data1.to_stream(stream, instance.frag_11)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version == 20)) or (((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20))):
			stream.write_ubytes(instance.padding)
		if instance.context.user_version.is_jwe and (instance.context.version == 19):
			stream.write_ubytes(instance.padding)

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
		return f'TexInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tex_info = {self.tex_info.__repr__()}'
		s += f'\n	* frag_00 = {self.frag_00.__repr__()}'
		s += f'\n	* frag_10 = {self.frag_10.__repr__()}'
		s += f'\n	* frag_01 = {self.frag_01.__repr__()}'
		s += f'\n	* frag_11 = {self.frag_11.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
