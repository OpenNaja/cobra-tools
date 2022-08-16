import generated.formats.base.basic
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LuaRoot(MemStruct):

	"""
	ZTUAC: 32 bytes
	newer: 48 bytes
	all meta data except lua size seems to just be meta data, can be zeroed
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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
		super().set_defaults()
		self.lua_size = 0
		self.sixteenk = 0
		self.hash = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		if self.context.version >= 18:
			self.source_path = Pointer(self.context, 0, generated.formats.base.basic.ZString)
			self.likely_alignment = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.lua_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.sixteenk = Uint.from_stream(stream, instance.context, 0, None)
		instance.hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_0 = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 18:
			instance.source_path = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
			instance.likely_alignment = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.zero_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zero_2 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.source_path, int):
			instance.source_path.arg = 0
		if not isinstance(instance.likely_alignment, int):
			instance.likely_alignment.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.lua_size)
		Uint.to_stream(stream, instance.sixteenk)
		Uint.to_stream(stream, instance.hash)
		Uint.to_stream(stream, instance.zero_0)
		if instance.context.version >= 18:
			Pointer.to_stream(stream, instance.source_path)
			Pointer.to_stream(stream, instance.likely_alignment)
		Uint64.to_stream(stream, instance.zero_1)
		Uint64.to_stream(stream, instance.zero_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'lua_size', Uint, (0, None), (False, None)
		yield 'sixteenk', Uint, (0, None), (False, None)
		yield 'hash', Uint, (0, None), (False, None)
		yield 'zero_0', Uint, (0, None), (False, None)
		if instance.context.version >= 18:
			yield 'source_path', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
			yield 'likely_alignment', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)
		yield 'zero_2', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'LuaRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* lua_size = {self.fmt_member(self.lua_size, indent+1)}'
		s += f'\n	* sixteenk = {self.fmt_member(self.sixteenk, indent+1)}'
		s += f'\n	* hash = {self.fmt_member(self.hash, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* source_path = {self.fmt_member(self.source_path, indent+1)}'
		s += f'\n	* likely_alignment = {self.fmt_member(self.likely_alignment, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* zero_2 = {self.fmt_member(self.zero_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
