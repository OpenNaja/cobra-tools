from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class LuaRoot(MemStruct):

	"""
	ZTUAC: 32 bytes
	newer: 48 bytes
	all meta data except lua size seems to just be meta data, can be zeroed
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.lua_size = 0
		self.sixteenk = 0
		self.hash = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.source_path = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.likely_alignment = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.lua_size = 0
		self.sixteenk = 0
		self.hash = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		if self.context.version >= 18:
			self.source_path = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if self.context.version >= 18:
			self.likely_alignment = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.lua_size = stream.read_uint()
		instance.sixteenk = stream.read_uint()
		instance.hash = stream.read_uint()
		instance.zero_0 = stream.read_uint()
		if instance.context.version >= 18:
			instance.source_path = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
			instance.likely_alignment = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.zero_1 = stream.read_uint64()
		instance.zero_2 = stream.read_uint64()
		instance.source_path.arg = 0
		instance.likely_alignment.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.lua_size)
		stream.write_uint(instance.sixteenk)
		stream.write_uint(instance.hash)
		stream.write_uint(instance.zero_0)
		if instance.context.version >= 18:
			Pointer.to_stream(stream, instance.source_path)
			Pointer.to_stream(stream, instance.likely_alignment)
		stream.write_uint64(instance.zero_1)
		stream.write_uint64(instance.zero_2)

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
		return f'LuaRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* lua_size = {fmt_member(self.lua_size, indent+1)}'
		s += f'\n	* sixteenk = {fmt_member(self.sixteenk, indent+1)}'
		s += f'\n	* hash = {fmt_member(self.hash, indent+1)}'
		s += f'\n	* zero_0 = {fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* source_path = {fmt_member(self.source_path, indent+1)}'
		s += f'\n	* likely_alignment = {fmt_member(self.likely_alignment, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
