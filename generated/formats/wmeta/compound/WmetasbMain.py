from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.wmeta.compound.EventEntry
import generated.formats.wmeta.compound.MediaEntry
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class WmetasbMain(MemStruct):

	"""
	# JWE, PC: 112 bytes
	# PZ, JWE2: 32 bytes
	todo - versioning that catches JWE1, needs wmetasb version from fileentry
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.hash = 0
		self.unk = 0
		self.events_count = 0
		self.hashes_count = 0
		self.media_count = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.media_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.bnk_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.events = ArrayPointer(self.context, self.events_count, generated.formats.wmeta.compound.EventEntry.EventEntry)
		self.hashes = ArrayPointer(self.context, self.hashes_count, generated.formats.base.basic.Uint)
		self.media = ArrayPointer(self.context, self.media_count, generated.formats.wmeta.compound.MediaEntry.MediaEntry)
		self.unused_2 = Pointer(self.context, 0, None)
		self.unused_3 = Pointer(self.context, 0, None)
		self.unused_4 = Pointer(self.context, 0, None)
		self.unused_5 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.hash = 0
		self.unk = 0
		self.events_count = 0
		if self.context.version <= 18:
			self.hashes_count = 0
		if self.context.version <= 18:
			self.media_count = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if self.context.version <= 18:
			self.media_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if self.context.version <= 18:
			self.bnk_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.events = ArrayPointer(self.context, self.events_count, generated.formats.wmeta.compound.EventEntry.EventEntry)
		if self.context.version <= 18:
			self.hashes = ArrayPointer(self.context, self.hashes_count, generated.formats.base.basic.Uint)
		if self.context.version <= 18:
			self.media = ArrayPointer(self.context, self.media_count, generated.formats.wmeta.compound.MediaEntry.MediaEntry)
		if self.context.version <= 18:
			self.unused_2 = Pointer(self.context, 0, None)
		if self.context.version <= 18:
			self.unused_3 = Pointer(self.context, 0, None)
		if self.context.version <= 18:
			self.unused_4 = Pointer(self.context, 0, None)
		if self.context.version <= 18:
			self.unused_5 = Pointer(self.context, 0, None)

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
		if instance.context.version <= 18:
			instance.media_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
			instance.bnk_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.events = ArrayPointer.from_stream(stream, instance.context, instance.events_count, generated.formats.wmeta.compound.EventEntry.EventEntry)
		instance.events_count = stream.read_uint64()
		if instance.context.version <= 18:
			instance.hashes = ArrayPointer.from_stream(stream, instance.context, instance.hashes_count, generated.formats.base.basic.Uint)
			instance.hashes_count = stream.read_uint64()
		if instance.context.version <= 18:
			instance.media = ArrayPointer.from_stream(stream, instance.context, instance.media_count, generated.formats.wmeta.compound.MediaEntry.MediaEntry)
			instance.media_count = stream.read_uint64()
		if instance.context.version <= 18:
			instance.unused_2 = Pointer.from_stream(stream, instance.context, 0, None)
			instance.unused_3 = Pointer.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 18:
			instance.unused_4 = Pointer.from_stream(stream, instance.context, 0, None)
			instance.unused_5 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.block_name.arg = 0
		instance.media_name.arg = 0
		instance.bnk_name.arg = 0
		instance.events.arg = instance.events_count
		instance.hashes.arg = instance.hashes_count
		instance.media.arg = instance.media_count
		instance.unused_2.arg = 0
		instance.unused_3.arg = 0
		instance.unused_4.arg = 0
		instance.unused_5.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.hash)
		stream.write_uint(instance.unk)
		Pointer.to_stream(stream, instance.block_name)
		if instance.context.version <= 18:
			Pointer.to_stream(stream, instance.media_name)
			Pointer.to_stream(stream, instance.bnk_name)
		ArrayPointer.to_stream(stream, instance.events)
		stream.write_uint64(instance.events_count)
		if instance.context.version <= 18:
			ArrayPointer.to_stream(stream, instance.hashes)
			stream.write_uint64(instance.hashes_count)
		if instance.context.version <= 18:
			ArrayPointer.to_stream(stream, instance.media)
			stream.write_uint64(instance.media_count)
		if instance.context.version <= 18:
			Pointer.to_stream(stream, instance.unused_2)
			Pointer.to_stream(stream, instance.unused_3)
		if instance.context.version <= 18:
			Pointer.to_stream(stream, instance.unused_4)
			Pointer.to_stream(stream, instance.unused_5)

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
		s += f'\n	* media_name = {fmt_member(self.media_name, indent+1)}'
		s += f'\n	* bnk_name = {fmt_member(self.bnk_name, indent+1)}'
		s += f'\n	* events = {fmt_member(self.events, indent+1)}'
		s += f'\n	* events_count = {fmt_member(self.events_count, indent+1)}'
		s += f'\n	* hashes = {fmt_member(self.hashes, indent+1)}'
		s += f'\n	* hashes_count = {fmt_member(self.hashes_count, indent+1)}'
		s += f'\n	* media = {fmt_member(self.media, indent+1)}'
		s += f'\n	* media_count = {fmt_member(self.media_count, indent+1)}'
		s += f'\n	* unused_2 = {fmt_member(self.unused_2, indent+1)}'
		s += f'\n	* unused_3 = {fmt_member(self.unused_3, indent+1)}'
		s += f'\n	* unused_4 = {fmt_member(self.unused_4, indent+1)}'
		s += f'\n	* unused_5 = {fmt_member(self.unused_5, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
