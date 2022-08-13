import generated.formats.tex.compound.SizeInfo
import generated.formats.tex.compound.TexBuffer
import generated.formats.tex.compound.TexBufferPc
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.tex.enums.DdsType import DdsType
from generated.formats.tex.enums.DdsTypeCoaster import DdsTypeCoaster


class TexHeader(MemStruct):

	"""
	DLA: 24 bytes, no pointers
	ZTUAC, PC: 24 bytes, with 1 pointer
	JWE, PZ, JWE2: 40 bytes, with 2 pointers
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_0 = 0
		self.zero_1 = 0
		self.compression_type = 0

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
		self.buffer_infos = 0
		self.size_info = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
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
			self.width = 0
			self.height = 0
		if self.context.version >= 17:
			self.stream_count = 0
			self.stream_count_repeat = 0
		self.pad = 0
		if self.context.version <= 15:
			self.pad_dla = 0
		if 17 <= self.context.version <= 18:
			self.buffer_infos = ArrayPointer(self.context, self.stream_count, generated.formats.tex.compound.TexBufferPc.TexBufferPc)
		if self.context.version >= 19:
			self.buffer_infos = ArrayPointer(self.context, self.stream_count, generated.formats.tex.compound.TexBuffer.TexBuffer)
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
			instance.compression_type = DdsTypeCoaster.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version < 19):
			instance.compression_type = DdsType.from_stream(stream, instance.context, 0, None)
		instance.one_0 = stream.read_ubyte()
		if instance.context.version <= 15:
			instance.num_mips = stream.read_ushort()
			instance.width = stream.read_ushort()
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
			DdsTypeCoaster.to_stream(stream, instance.compression_type)
		if not (instance.context.version < 19):
			DdsType.to_stream(stream, instance.compression_type)
		stream.write_ubyte(instance.one_0)
		if instance.context.version <= 15:
			stream.write_ushort(instance.num_mips)
			stream.write_ushort(instance.width)
			stream.write_ushort(instance.height)
		if instance.context.version >= 17:
			stream.write_ubyte(instance.stream_count)
			stream.write_ubyte(instance.stream_count_repeat)
		stream.write_uint(instance.pad)
		if instance.context.version <= 15:
			stream.write_uint64(instance.pad_dla)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		if instance.context.version <= 15:
			yield ('zero_0', Uint, (0, None))
		if instance.context.version >= 17:
			yield ('zero_0', Uint64, (0, None))
		if instance.context.version >= 19:
			yield ('zero_1', Uint64, (0, None))
		if 17 <= instance.context.version <= 18:
			yield ('buffer_infos', ArrayPointer, (instance.stream_count, generated.formats.tex.compound.TexBufferPc.TexBufferPc))
		if instance.context.version >= 19:
			yield ('buffer_infos', ArrayPointer, (instance.stream_count, generated.formats.tex.compound.TexBuffer.TexBuffer))
			yield ('size_info', Pointer, (0, generated.formats.tex.compound.SizeInfo.SizeInfo))
		if instance.context.version < 19:
			yield ('compression_type', DdsTypeCoaster, (0, None))
		if not (instance.context.version < 19):
			yield ('compression_type', DdsType, (0, None))
		yield ('one_0', Ubyte, (0, None))
		if instance.context.version <= 15:
			yield ('num_mips', Ushort, (0, None))
			yield ('width', Ushort, (0, None))
			yield ('height', Ushort, (0, None))
		if instance.context.version >= 17:
			yield ('stream_count', Ubyte, (0, None))
			yield ('stream_count_repeat', Ubyte, (0, None))
		yield ('pad', Uint, (0, None))
		if instance.context.version <= 15:
			yield ('pad_dla', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'TexHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* buffer_infos = {self.fmt_member(self.buffer_infos, indent+1)}'
		s += f'\n	* size_info = {self.fmt_member(self.size_info, indent+1)}'
		s += f'\n	* compression_type = {self.fmt_member(self.compression_type, indent+1)}'
		s += f'\n	* one_0 = {self.fmt_member(self.one_0, indent+1)}'
		s += f'\n	* num_mips = {self.fmt_member(self.num_mips, indent+1)}'
		s += f'\n	* width = {self.fmt_member(self.width, indent+1)}'
		s += f'\n	* height = {self.fmt_member(self.height, indent+1)}'
		s += f'\n	* stream_count = {self.fmt_member(self.stream_count, indent+1)}'
		s += f'\n	* stream_count_repeat = {self.fmt_member(self.stream_count_repeat, indent+1)}'
		s += f'\n	* pad = {self.fmt_member(self.pad, indent+1)}'
		s += f'\n	* pad_dla = {self.fmt_member(self.pad_dla, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
