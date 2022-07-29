from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class MediaEntry(MemStruct):

	"""
	PC: 32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.hash = 0
		self.zero = 0
		self.block_name = 0
		self.wav_name = 0
		self.wem_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.hash = 0
		self.zero = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.wav_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.wem_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.hash = stream.read_uint()
		instance.zero = stream.read_uint()
		instance.block_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.wav_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.wem_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.block_name.arg = 0
		instance.wav_name.arg = 0
		instance.wem_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.hash)
		stream.write_uint(instance.zero)
		Pointer.to_stream(stream, instance.block_name)
		Pointer.to_stream(stream, instance.wav_name)
		Pointer.to_stream(stream, instance.wem_name)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('hash', Uint, (0, None))
		yield ('zero', Uint, (0, None))
		yield ('block_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('wav_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('wem_name', Pointer, (0, generated.formats.base.basic.ZString))

	def get_info_str(self, indent=0):
		return f'MediaEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* hash = {fmt_member(self.hash, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* block_name = {fmt_member(self.block_name, indent+1)}'
		s += f'\n	* wav_name = {fmt_member(self.wav_name, indent+1)}'
		s += f'\n	* wem_name = {fmt_member(self.wem_name, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
