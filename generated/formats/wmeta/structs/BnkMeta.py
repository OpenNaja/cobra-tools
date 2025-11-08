from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.wmeta.imports import name_type_map


class BnkMeta(MemStruct):

	"""
	# JWE, PC: 112 bytes
	"""

	__name__ = 'BnkMeta'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = name_type_map['Uint'](self.context, 0, None)
		self._padding = name_type_map['Uint'].from_value(0)
		self.events_count = name_type_map['Uint64'](self.context, 0, None)
		self.hashes_count = name_type_map['Uint64'](self.context, 0, None)
		self.media_count = name_type_map['Uint64'](self.context, 0, None)
		self.unused_2 = name_type_map['Uint64'](self.context, 0, None)
		self.unused_3 = name_type_map['Uint64'](self.context, 0, None)
		self.unused_4 = name_type_map['Uint64'](self.context, 0, None)
		self.unused_5 = name_type_map['Uint64'](self.context, 0, None)
		self.type_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.bnk_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.file_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.events = name_type_map['ArrayPointer'](self.context, self.events_count, name_type_map['EventEntry'])
		self.hashes = name_type_map['ArrayPointer'](self.context, self.hashes_count, name_type_map['Uint'])
		self.media = name_type_map['ArrayPointer'](self.context, self.media_count, name_type_map['MediaEntry'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'hash', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield '_padding', name_type_map['Uint'], (0, None), (False, 0), (None, None)
		yield 'type_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'bnk_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'file_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'events', name_type_map['ArrayPointer'], (None, name_type_map['EventEntry']), (False, None), (None, None)
		yield 'events_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'hashes', name_type_map['ArrayPointer'], (None, name_type_map['Uint']), (False, None), (None, None)
		yield 'hashes_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'media', name_type_map['ArrayPointer'], (None, name_type_map['MediaEntry']), (False, None), (None, None)
		yield 'media_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unused_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unused_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unused_4', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unused_5', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'hash', name_type_map['Uint'], (0, None), (False, None)
		yield '_padding', name_type_map['Uint'], (0, None), (False, 0)
		yield 'type_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'bnk_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'file_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'events', name_type_map['ArrayPointer'], (instance.events_count, name_type_map['EventEntry']), (False, None)
		yield 'events_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'hashes', name_type_map['ArrayPointer'], (instance.hashes_count, name_type_map['Uint']), (False, None)
		yield 'hashes_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'media', name_type_map['ArrayPointer'], (instance.media_count, name_type_map['MediaEntry']), (False, None)
		yield 'media_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unused_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unused_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unused_4', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unused_5', name_type_map['Uint64'], (0, None), (False, None)
