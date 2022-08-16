import generated.formats.base.basic
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MediaEntry(MemStruct):

	"""
	PC: 32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = 0
		self.zero = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.wav_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.wem_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.hash = 0
		self.zero = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.wav_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.wem_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero = Uint.from_stream(stream, instance.context, 0, None)
		instance.block_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.wav_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.wem_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.block_name, int):
			instance.block_name.arg = 0
		if not isinstance(instance.wav_name, int):
			instance.wav_name.arg = 0
		if not isinstance(instance.wem_name, int):
			instance.wem_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.hash)
		Uint.to_stream(stream, instance.zero)
		Pointer.to_stream(stream, instance.block_name)
		Pointer.to_stream(stream, instance.wav_name)
		Pointer.to_stream(stream, instance.wem_name)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'hash', Uint, (0, None), (False, None)
		yield 'zero', Uint, (0, None), (False, None)
		yield 'block_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'wav_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'wem_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'MediaEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* hash = {self.fmt_member(self.hash, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* block_name = {self.fmt_member(self.block_name, indent+1)}'
		s += f'\n	* wav_name = {self.fmt_member(self.wav_name, indent+1)}'
		s += f'\n	* wem_name = {self.fmt_member(self.wem_name, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
