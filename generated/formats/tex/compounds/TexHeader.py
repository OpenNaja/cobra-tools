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

		# 0; 1 for PC
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
		if self.context.version <= 18:
			self.compression_type = DdsTypeCoaster(self.context, 0, None)
		if self.context.version >= 19:
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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
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
		if instance.context.version <= 18:
			yield 'compression_type', DdsTypeCoaster, (0, None), (False, None)
		if instance.context.version >= 19:
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
