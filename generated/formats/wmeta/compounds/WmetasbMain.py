import generated.formats.base.basic
import generated.formats.wmeta.compounds.EventEntry
import generated.formats.wmeta.compounds.MediaEntry
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class WmetasbMain(MemStruct):

	"""
	# JWE, PC: 112 bytes
	# PZ, JWE2: 32 bytes
	todo - versioning that catches JWE1, needs wmetasb version from fileentry
	"""

	__name__ = WmetasbMain

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = 0
		self.unk = 0
		self.events_count = 0
		self.hashes_count = 0
		self.media_count = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.media_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.bnk_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.events = ArrayPointer(self.context, self.events_count, generated.formats.wmeta.compounds.EventEntry.EventEntry)
		self.hashes = ArrayPointer(self.context, self.hashes_count, generated.formats.base.basic.Uint)
		self.media = ArrayPointer(self.context, self.media_count, generated.formats.wmeta.compounds.MediaEntry.MediaEntry)
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
			self.media_count = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if self.context.version <= 18:
			self.media_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
			self.bnk_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.events = ArrayPointer(self.context, self.events_count, generated.formats.wmeta.compounds.EventEntry.EventEntry)
		if self.context.version <= 18:
			self.hashes = ArrayPointer(self.context, self.hashes_count, generated.formats.base.basic.Uint)
			self.media = ArrayPointer(self.context, self.media_count, generated.formats.wmeta.compounds.MediaEntry.MediaEntry)
			self.unused_2 = Pointer(self.context, 0, None)
			self.unused_3 = Pointer(self.context, 0, None)
			self.unused_4 = Pointer(self.context, 0, None)
			self.unused_5 = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk = Uint.from_stream(stream, instance.context, 0, None)
		instance.block_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if instance.context.version <= 18:
			instance.media_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
			instance.bnk_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.events = ArrayPointer.from_stream(stream, instance.context, instance.events_count, generated.formats.wmeta.compounds.EventEntry.EventEntry)
		instance.events_count = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 18:
			instance.hashes = ArrayPointer.from_stream(stream, instance.context, instance.hashes_count, generated.formats.base.basic.Uint)
			instance.hashes_count = Uint64.from_stream(stream, instance.context, 0, None)
			instance.media = ArrayPointer.from_stream(stream, instance.context, instance.media_count, generated.formats.wmeta.compounds.MediaEntry.MediaEntry)
			instance.media_count = Uint64.from_stream(stream, instance.context, 0, None)
			instance.unused_2 = Pointer.from_stream(stream, instance.context, 0, None)
			instance.unused_3 = Pointer.from_stream(stream, instance.context, 0, None)
			instance.unused_4 = Pointer.from_stream(stream, instance.context, 0, None)
			instance.unused_5 = Pointer.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.block_name, int):
			instance.block_name.arg = 0
		if not isinstance(instance.media_name, int):
			instance.media_name.arg = 0
		if not isinstance(instance.bnk_name, int):
			instance.bnk_name.arg = 0
		if not isinstance(instance.events, int):
			instance.events.arg = instance.events_count
		if not isinstance(instance.hashes, int):
			instance.hashes.arg = instance.hashes_count
		if not isinstance(instance.media, int):
			instance.media.arg = instance.media_count
		if not isinstance(instance.unused_2, int):
			instance.unused_2.arg = 0
		if not isinstance(instance.unused_3, int):
			instance.unused_3.arg = 0
		if not isinstance(instance.unused_4, int):
			instance.unused_4.arg = 0
		if not isinstance(instance.unused_5, int):
			instance.unused_5.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.hash)
		Uint.to_stream(stream, instance.unk)
		Pointer.to_stream(stream, instance.block_name)
		if instance.context.version <= 18:
			Pointer.to_stream(stream, instance.media_name)
			Pointer.to_stream(stream, instance.bnk_name)
		ArrayPointer.to_stream(stream, instance.events)
		Uint64.to_stream(stream, instance.events_count)
		if instance.context.version <= 18:
			ArrayPointer.to_stream(stream, instance.hashes)
			Uint64.to_stream(stream, instance.hashes_count)
			ArrayPointer.to_stream(stream, instance.media)
			Uint64.to_stream(stream, instance.media_count)
			Pointer.to_stream(stream, instance.unused_2)
			Pointer.to_stream(stream, instance.unused_3)
			Pointer.to_stream(stream, instance.unused_4)
			Pointer.to_stream(stream, instance.unused_5)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'hash', Uint, (0, None), (False, None)
		yield 'unk', Uint, (0, None), (False, None)
		yield 'block_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		if instance.context.version <= 18:
			yield 'media_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
			yield 'bnk_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'events', ArrayPointer, (instance.events_count, generated.formats.wmeta.compounds.EventEntry.EventEntry), (False, None)
		yield 'events_count', Uint64, (0, None), (False, None)
		if instance.context.version <= 18:
			yield 'hashes', ArrayPointer, (instance.hashes_count, generated.formats.base.basic.Uint), (False, None)
			yield 'hashes_count', Uint64, (0, None), (False, None)
			yield 'media', ArrayPointer, (instance.media_count, generated.formats.wmeta.compounds.MediaEntry.MediaEntry), (False, None)
			yield 'media_count', Uint64, (0, None), (False, None)
			yield 'unused_2', Pointer, (0, None), (False, None)
			yield 'unused_3', Pointer, (0, None), (False, None)
			yield 'unused_4', Pointer, (0, None), (False, None)
			yield 'unused_5', Pointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'WmetasbMain [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* hash = {self.fmt_member(self.hash, indent+1)}'
		s += f'\n	* unk = {self.fmt_member(self.unk, indent+1)}'
		s += f'\n	* block_name = {self.fmt_member(self.block_name, indent+1)}'
		s += f'\n	* media_name = {self.fmt_member(self.media_name, indent+1)}'
		s += f'\n	* bnk_name = {self.fmt_member(self.bnk_name, indent+1)}'
		s += f'\n	* events = {self.fmt_member(self.events, indent+1)}'
		s += f'\n	* events_count = {self.fmt_member(self.events_count, indent+1)}'
		s += f'\n	* hashes = {self.fmt_member(self.hashes, indent+1)}'
		s += f'\n	* hashes_count = {self.fmt_member(self.hashes_count, indent+1)}'
		s += f'\n	* media = {self.fmt_member(self.media, indent+1)}'
		s += f'\n	* media_count = {self.fmt_member(self.media_count, indent+1)}'
		s += f'\n	* unused_2 = {self.fmt_member(self.unused_2, indent+1)}'
		s += f'\n	* unused_3 = {self.fmt_member(self.unused_3, indent+1)}'
		s += f'\n	* unused_4 = {self.fmt_member(self.unused_4, indent+1)}'
		s += f'\n	* unused_5 = {self.fmt_member(self.unused_5, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
