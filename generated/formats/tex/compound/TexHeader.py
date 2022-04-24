from source.formats.base.basic import fmt_member
import generated.formats.tex.compound.SizeInfo
import generated.formats.tex.compound.TexBuffer
import generated.formats.tex.compound.TexBufferPc
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.tex.enum.DdsType import DdsType
from generated.formats.tex.enum.DdsTypeCoaster import DdsTypeCoaster


class TexHeader(MemStruct):

	"""
	DLA: 24 bytes, no pointers
	ZTUAC, PC: 24 bytes, with 1 pointer
	JWE, PZ, JWE2: 40 bytes, with 2 pointers
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero_0 = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.compression_type = DdsTypeCoaster(self.context, 0, None)
		self.compression_type = DdsType(self.context, 0, None)

		# 0 or 1
		self.one_0 = 0
		self.num_mips = 0
		self.width = 0
		self.height = 0

		# amount of files combined in this texture, usually 1 or 2, 3 for JWE2 rex
		self.stream_count = 0

		# usually as above
		self.stream_count_repeat = 0

		# 0
		self.pad = 0
		self.pad_dla = 0
		self.buffer_infos = ArrayPointer(self.context, self.stream_count, generated.formats.tex.compound.TexBufferPc.TexBufferPc)
		self.buffer_infos = ArrayPointer(self.context, self.stream_count, generated.formats.tex.compound.TexBuffer.TexBuffer)
		self.size_info = Pointer(self.context, 0, generated.formats.tex.compound.SizeInfo.SizeInfo)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 15:
			self.zero_0 = 0
		if self.context.version >= 17:
			self.zero_0 = 0
		if self.context.version >= 19:
			self.zero_1 = 0
		if self.context.version < 19:
			self.compression_type = DdsTypeCoaster(self.context, 0, None)
		if not (self.context.version < 19):
			self.compression_type = DdsType(self.context, 0, None)
		self.one_0 = 0
		if self.context.version <= 15:
			self.num_mips = 0
		if self.context.version <= 15:
			self.width = 0
		if self.context.version <= 15:
			self.height = 0
		if self.context.version >= 17:
			self.stream_count = 0
		if self.context.version >= 17:
			self.stream_count_repeat = 0
		self.pad = 0
		if self.context.version <= 15:
			self.pad_dla = 0
		if 17 <= self.context.version <= 18:
			self.buffer_infos = ArrayPointer(self.context, self.stream_count, generated.formats.tex.compound.TexBufferPc.TexBufferPc)
		if self.context.version >= 19:
			self.buffer_infos = ArrayPointer(self.context, self.stream_count, generated.formats.tex.compound.TexBuffer.TexBuffer)
		if self.context.version >= 19:
			self.size_info = Pointer(self.context, 0, generated.formats.tex.compound.SizeInfo.SizeInfo)

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
		if instance.context.version <= 15:
			instance.zero_0 = stream.read_uint()
		if instance.context.version >= 17:
			instance.zero_0 = stream.read_uint64()
		if instance.context.version >= 19:
			instance.zero_1 = stream.read_uint64()
		if 17 <= instance.context.version <= 18:
			instance.buffer_infos = ArrayPointer.from_stream(stream, instance.context, instance.stream_count, generated.formats.tex.compound.TexBufferPc.TexBufferPc)
		if instance.context.version >= 19:
			instance.buffer_infos = ArrayPointer.from_stream(stream, instance.context, instance.stream_count, generated.formats.tex.compound.TexBuffer.TexBuffer)
			instance.size_info = Pointer.from_stream(stream, instance.context, 0, generated.formats.tex.compound.SizeInfo.SizeInfo)
		if instance.context.version < 19:
			instance.compression_type = DdsTypeCoaster.from_value(stream.read_ubyte())
		if not (instance.context.version < 19):
			instance.compression_type = DdsType.from_value(stream.read_ubyte())
		instance.one_0 = stream.read_ubyte()
		if instance.context.version <= 15:
			instance.num_mips = stream.read_ushort()
			instance.width = stream.read_ushort()
		if instance.context.version <= 15:
			instance.height = stream.read_ushort()
		if instance.context.version >= 17:
			instance.stream_count = stream.read_ubyte()
			instance.stream_count_repeat = stream.read_ubyte()
		instance.pad = stream.read_uint()
		if instance.context.version <= 15:
			instance.pad_dla = stream.read_uint64()
		instance.buffer_infos.arg = instance.stream_count
		instance.buffer_infos.arg = instance.stream_count
		instance.size_info.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 15:
			stream.write_uint(instance.zero_0)
		if instance.context.version >= 17:
			stream.write_uint64(instance.zero_0)
		if instance.context.version >= 19:
			stream.write_uint64(instance.zero_1)
		if 17 <= instance.context.version <= 18:
			ArrayPointer.to_stream(stream, instance.buffer_infos)
		if instance.context.version >= 19:
			ArrayPointer.to_stream(stream, instance.buffer_infos)
			Pointer.to_stream(stream, instance.size_info)
		if instance.context.version < 19:
			stream.write_ubyte(instance.compression_type.value)
		if not (instance.context.version < 19):
			stream.write_ubyte(instance.compression_type.value)
		stream.write_ubyte(instance.one_0)
		if instance.context.version <= 15:
			stream.write_ushort(instance.num_mips)
			stream.write_ushort(instance.width)
		if instance.context.version <= 15:
			stream.write_ushort(instance.height)
		if instance.context.version >= 17:
			stream.write_ubyte(instance.stream_count)
			stream.write_ubyte(instance.stream_count_repeat)
		stream.write_uint(instance.pad)
		if instance.context.version <= 15:
			stream.write_uint64(instance.pad_dla)

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
		return f'TexHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero_0 = {fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* buffer_infos = {fmt_member(self.buffer_infos, indent+1)}'
		s += f'\n	* size_info = {fmt_member(self.size_info, indent+1)}'
		s += f'\n	* compression_type = {fmt_member(self.compression_type, indent+1)}'
		s += f'\n	* one_0 = {fmt_member(self.one_0, indent+1)}'
		s += f'\n	* num_mips = {fmt_member(self.num_mips, indent+1)}'
		s += f'\n	* width = {fmt_member(self.width, indent+1)}'
		s += f'\n	* height = {fmt_member(self.height, indent+1)}'
		s += f'\n	* stream_count = {fmt_member(self.stream_count, indent+1)}'
		s += f'\n	* stream_count_repeat = {fmt_member(self.stream_count_repeat, indent+1)}'
		s += f'\n	* pad = {fmt_member(self.pad, indent+1)}'
		s += f'\n	* pad_dla = {fmt_member(self.pad_dla, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
