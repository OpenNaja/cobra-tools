from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.wmeta.imports import name_type_map


class BnkMetaNew(MemStruct):

	"""
	PZ, JWE2, PC2: 32 bytes
	"""

	__name__ = 'BnkMetaNew'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = name_type_map['Uint'](self.context, 0, None)
		self.padding = name_type_map['Uint'].from_value(0)
		self.events_count = name_type_map['Uint'](self.context, 0, None)
		self.hash = name_type_map['Uint'](self.context, 0, None)

		# 0 or 1
		self.flag = name_type_map['Uint'](self.context, 0, None)
		self.unk_2 = name_type_map['Uint'](self.context, 0, None)
		self.type_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.events = name_type_map['ArrayPointer'](self.context, self.events_count, name_type_map['EventEntry'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'hash', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.is_pz, None)
		yield 'padding', name_type_map['Uint'], (0, None), (True, 0), (lambda context: context.is_pz, None)
		yield 'type_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'events', name_type_map['ArrayPointer'], (None, name_type_map['EventEntry']), (False, None), (None, None)
		yield 'events_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'hash', name_type_map['Uint'], (0, None), (False, None), (lambda context: not context.is_pz, None)
		yield 'flag', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Uint'], (0, None), (False, None), (lambda context: not context.is_pz, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.is_pz:
			yield 'hash', name_type_map['Uint'], (0, None), (False, None)
			yield 'padding', name_type_map['Uint'], (0, None), (True, 0)
		yield 'type_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'events', name_type_map['ArrayPointer'], (instance.events_count, name_type_map['EventEntry']), (False, None)
		yield 'events_count', name_type_map['Uint'], (0, None), (False, None)
		if not instance.context.is_pz:
			yield 'hash', name_type_map['Uint'], (0, None), (False, None)
		yield 'flag', name_type_map['Uint'], (0, None), (False, None)
		if not instance.context.is_pz:
			yield 'unk_2', name_type_map['Uint'], (0, None), (False, None)
