from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class WmetasbMain(MemStruct):

	"""
	# JWE, PC: 112 bytes
	# PZ, JWE2: 32 bytes
	todo - versioning that catches JWE1, needs wmetasb version from fileentry
	"""

	__name__ = 'WmetasbMain'

	_import_key = 'wmeta.compounds.WmetasbMain'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = 0
		self.unk = 0
		self.events_count = 0
		self.hashes_count = 0
		self.media_count = 0
		self.block_name = Pointer(self.context, 0, ZString)
		self.media_name = Pointer(self.context, 0, ZString)
		self.bnk_name = Pointer(self.context, 0, ZString)
		self.events = ArrayPointer(self.context, self.events_count, WmetasbMain._import_map["wmeta.compounds.EventEntry"])
		self.hashes = ArrayPointer(self.context, self.hashes_count, Uint)
		self.media = ArrayPointer(self.context, self.media_count, WmetasbMain._import_map["wmeta.compounds.MediaEntry"])
		self.unused_2 = Pointer(self.context, 0, None)
		self.unused_3 = Pointer(self.context, 0, None)
		self.unused_4 = Pointer(self.context, 0, None)
		self.unused_5 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('hash', Uint, (0, None), (False, None), None)
		yield ('unk', Uint, (0, None), (False, None), None)
		yield ('block_name', Pointer, (0, ZString), (False, None), None)
		yield ('media_name', Pointer, (0, ZString), (False, None), True)
		yield ('bnk_name', Pointer, (0, ZString), (False, None), True)
		yield ('events', ArrayPointer, (None, WmetasbMain._import_map["wmeta.compounds.EventEntry"]), (False, None), None)
		yield ('events_count', Uint64, (0, None), (False, None), None)
		yield ('hashes', ArrayPointer, (None, Uint), (False, None), True)
		yield ('hashes_count', Uint64, (0, None), (False, None), True)
		yield ('media', ArrayPointer, (None, WmetasbMain._import_map["wmeta.compounds.MediaEntry"]), (False, None), True)
		yield ('media_count', Uint64, (0, None), (False, None), True)
		yield ('unused_2', Pointer, (0, None), (False, None), True)
		yield ('unused_3', Pointer, (0, None), (False, None), True)
		yield ('unused_4', Pointer, (0, None), (False, None), True)
		yield ('unused_5', Pointer, (0, None), (False, None), True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'hash', Uint, (0, None), (False, None)
		yield 'unk', Uint, (0, None), (False, None)
		yield 'block_name', Pointer, (0, ZString), (False, None)
		if instance.context.version <= 18:
			yield 'media_name', Pointer, (0, ZString), (False, None)
			yield 'bnk_name', Pointer, (0, ZString), (False, None)
		yield 'events', ArrayPointer, (instance.events_count, WmetasbMain._import_map["wmeta.compounds.EventEntry"]), (False, None)
		yield 'events_count', Uint64, (0, None), (False, None)
		if instance.context.version <= 18:
			yield 'hashes', ArrayPointer, (instance.hashes_count, Uint), (False, None)
			yield 'hashes_count', Uint64, (0, None), (False, None)
			yield 'media', ArrayPointer, (instance.media_count, WmetasbMain._import_map["wmeta.compounds.MediaEntry"]), (False, None)
			yield 'media_count', Uint64, (0, None), (False, None)
			yield 'unused_2', Pointer, (0, None), (False, None)
			yield 'unused_3', Pointer, (0, None), (False, None)
			yield 'unused_4', Pointer, (0, None), (False, None)
			yield 'unused_5', Pointer, (0, None), (False, None)


WmetasbMain.init_attributes()
