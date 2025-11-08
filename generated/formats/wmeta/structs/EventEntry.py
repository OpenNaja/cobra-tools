from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.wmeta.imports import name_type_map


class EventEntry(MemStruct):

	"""
	PC, JWE1: 56 bytes
	PZ, JWE2: 40 bytes
	PC2: 44 bytes
	"""

	__name__ = 'EventEntry'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = name_type_map['Uint'](self.context, 0, None)

		# not padding on pz?!
		self.padding = name_type_map['Uint'].from_value(0)
		self.float = name_type_map['Float'](self.context, 0, None)
		self.flag_0 = name_type_map['Uint'](self.context, 0, None)
		self.flag_1 = name_type_map['Uint'](self.context, 0, None)
		self.flag_2 = name_type_map['Uint'](self.context, 0, None)
		self.zero_2 = name_type_map['Uint'].from_value(0)
		self.hash_b = name_type_map['Uint'](self.context, 0, None)
		self.hash_c = name_type_map['Uint'](self.context, 0, None)
		self.zero_4 = name_type_map['Uint'].from_value(0)
		self.u_2 = name_type_map['Uint'](self.context, 0, None)
		self.u_1 = name_type_map['Uint'](self.context, 0, None)
		self.u_4 = name_type_map['Uint'](self.context, 0, None)
		self.event_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# used in stop events
		self.start_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'hash', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'padding', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'event_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: context.version <= 1, None)
		yield 'float', name_type_map['Float'], (0, None), (False, None), (lambda context: context.version <= 1, None)
		yield 'flag_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'flag_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'flag_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'start_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: context.version <= 1, None)
		yield 'zero_2', name_type_map['Uint'], (0, None), (True, 0), (lambda context: context.version <= 1, None)
		yield 'hash_b', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'hash_c', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zero_4', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'u_2', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 2, None)
		yield 'u_1', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 2, None)
		yield 'u_4', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 2 and context.is_pc_2, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'hash', name_type_map['Uint'], (0, None), (False, None)
		yield 'padding', name_type_map['Uint'], (0, None), (True, 0)
		if instance.context.version <= 1:
			yield 'event_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'float', name_type_map['Float'], (0, None), (False, None)
		yield 'flag_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'flag_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'flag_2', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version <= 1:
			yield 'start_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'zero_2', name_type_map['Uint'], (0, None), (True, 0)
		yield 'hash_b', name_type_map['Uint'], (0, None), (False, None)
		yield 'hash_c', name_type_map['Uint'], (0, None), (False, None)
		yield 'zero_4', name_type_map['Uint'], (0, None), (True, 0)
		if instance.context.version >= 2:
			yield 'u_2', name_type_map['Uint'], (0, None), (False, None)
			yield 'u_1', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version >= 2 and instance.context.is_pc_2:
			yield 'u_4', name_type_map['Uint'], (0, None), (False, None)
