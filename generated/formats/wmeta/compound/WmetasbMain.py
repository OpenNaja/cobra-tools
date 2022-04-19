from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.wmeta.compound.WmetasbChild
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class WmetasbMain(MemStruct):

	"""
	# JWE: 112 bytes??
	# PZ, JWE2: 32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.hash = 0
		self.unk = 0
		self.count = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.next_levels = ArrayPointer(self.context, self.count, generated.formats.wmeta.compound.WmetasbChild.WmetasbChild)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.hash = 0
		self.unk = 0
		self.count = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.next_levels = ArrayPointer(self.context, self.count, generated.formats.wmeta.compound.WmetasbChild.WmetasbChild)

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
		instance.unk = stream.read_uint()
		instance.block_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.next_levels = ArrayPointer.from_stream(stream, instance.context, instance.count, generated.formats.wmeta.compound.WmetasbChild.WmetasbChild)
		instance.count = stream.read_uint64()
		instance.block_name.arg = 0
		instance.next_levels.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.hash)
		stream.write_uint(instance.unk)
		Pointer.to_stream(stream, instance.block_name)
		ArrayPointer.to_stream(stream, instance.next_levels)
		stream.write_uint64(instance.count)

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
		return f'WmetasbMain [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* hash = {fmt_member(self.hash, indent+1)}'
		s += f'\n	* unk = {fmt_member(self.unk, indent+1)}'
		s += f'\n	* block_name = {fmt_member(self.block_name, indent+1)}'
		s += f'\n	* next_levels = {fmt_member(self.next_levels, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
