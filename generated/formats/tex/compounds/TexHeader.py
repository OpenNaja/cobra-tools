from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.tex.enums.DdsType import DdsType
from generated.formats.tex.enums.DdsTypeCoaster import DdsTypeCoaster


class TexHeader(MemStruct):

	"""
	DLA: 24 bytes, no pointers
	ZTUAC, PC: 24 bytes, with 1 pointer
	JWE, PZ, JWE2: 40 bytes, with 2 pointers
	"""

	__name__ = 'TexHeader'

	_import_path = 'generated.formats.tex.compounds.TexHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_0 = 0
		self.zero_1 = 0
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
		self.buffer_infos = ArrayPointer(self.context, self.stream_count, TexHeader._import_path_map["generated.formats.tex.compounds.TexBuffer"])
		self.size_info = Pointer(self.context, 0, TexHeader._import_path_map["generated.formats.tex.compounds.SizeInfo"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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
			self.buffer_infos = ArrayPointer(self.context, self.stream_count, TexHeader._import_path_map["generated.formats.tex.compounds.TexBufferPc"])
		if self.context.version >= 19:
			self.buffer_infos = ArrayPointer(self.context, self.stream_count, TexHeader._import_path_map["generated.formats.tex.compounds.TexBuffer"])
			self.size_info = Pointer(self.context, 0, TexHeader._import_path_map["generated.formats.tex.compounds.SizeInfo"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.context.version <= 15:
			instance.zero_0 = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 17:
			instance.zero_0 = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 19:
			instance.zero_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if 17 <= instance.context.version <= 18:
			instance.buffer_infos = ArrayPointer.from_stream(stream, instance.context, instance.stream_count, TexHeader._import_path_map["generated.formats.tex.compounds.TexBufferPc"])
		if instance.context.version >= 19:
			instance.buffer_infos = ArrayPointer.from_stream(stream, instance.context, instance.stream_count, TexHeader._import_path_map["generated.formats.tex.compounds.TexBuffer"])
			instance.size_info = Pointer.from_stream(stream, instance.context, 0, TexHeader._import_path_map["generated.formats.tex.compounds.SizeInfo"])
		if instance.context.version < 19:
			instance.compression_type = DdsTypeCoaster.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version < 19):
			instance.compression_type = DdsType.from_stream(stream, instance.context, 0, None)
		instance.one_0 = Ubyte.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 15:
			instance.num_mips = Ushort.from_stream(stream, instance.context, 0, None)
			instance.width = Ushort.from_stream(stream, instance.context, 0, None)
			instance.height = Ushort.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 17:
			instance.stream_count = Ubyte.from_stream(stream, instance.context, 0, None)
			instance.stream_count_repeat = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.pad = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 15:
			instance.pad_dla = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.buffer_infos, int):
			instance.buffer_infos.arg = instance.stream_count
		if not isinstance(instance.buffer_infos, int):
			instance.buffer_infos.arg = instance.stream_count
		if not isinstance(instance.size_info, int):
			instance.size_info.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 15:
			Uint.to_stream(stream, instance.zero_0)
		if instance.context.version >= 17:
			Uint64.to_stream(stream, instance.zero_0)
		if instance.context.version >= 19:
			Uint64.to_stream(stream, instance.zero_1)
		if 17 <= instance.context.version <= 18:
			ArrayPointer.to_stream(stream, instance.buffer_infos)
		if instance.context.version >= 19:
			ArrayPointer.to_stream(stream, instance.buffer_infos)
			Pointer.to_stream(stream, instance.size_info)
		if instance.context.version < 19:
			DdsTypeCoaster.to_stream(stream, instance.compression_type)
		if not (instance.context.version < 19):
			DdsType.to_stream(stream, instance.compression_type)
		Ubyte.to_stream(stream, instance.one_0)
		if instance.context.version <= 15:
			Ushort.to_stream(stream, instance.num_mips)
			Ushort.to_stream(stream, instance.width)
			Ushort.to_stream(stream, instance.height)
		if instance.context.version >= 17:
			Ubyte.to_stream(stream, instance.stream_count)
			Ubyte.to_stream(stream, instance.stream_count_repeat)
		Uint.to_stream(stream, instance.pad)
		if instance.context.version <= 15:
			Uint64.to_stream(stream, instance.pad_dla)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		if instance.context.version <= 15:
			yield 'zero_0', Uint, (0, None), (False, None)
		if instance.context.version >= 17:
			yield 'zero_0', Uint64, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'zero_1', Uint64, (0, None), (False, None)
		if 17 <= instance.context.version <= 18:
			yield 'buffer_infos', ArrayPointer, (instance.stream_count, TexHeader._import_path_map["generated.formats.tex.compounds.TexBufferPc"]), (False, None)
		if instance.context.version >= 19:
			yield 'buffer_infos', ArrayPointer, (instance.stream_count, TexHeader._import_path_map["generated.formats.tex.compounds.TexBuffer"]), (False, None)
			yield 'size_info', Pointer, (0, TexHeader._import_path_map["generated.formats.tex.compounds.SizeInfo"]), (False, None)
		if instance.context.version < 19:
			yield 'compression_type', DdsTypeCoaster, (0, None), (False, None)
		if not (instance.context.version < 19):
			yield 'compression_type', DdsType, (0, None), (False, None)
		yield 'one_0', Ubyte, (0, None), (False, None)
		if instance.context.version <= 15:
			yield 'num_mips', Ushort, (0, None), (False, None)
			yield 'width', Ushort, (0, None), (False, None)
			yield 'height', Ushort, (0, None), (False, None)
		if instance.context.version >= 17:
			yield 'stream_count', Ubyte, (0, None), (False, None)
			yield 'stream_count_repeat', Ubyte, (0, None), (False, None)
		yield 'pad', Uint, (0, None), (False, None)
		if instance.context.version <= 15:
			yield 'pad_dla', Uint64, (0, None), (False, None)

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
