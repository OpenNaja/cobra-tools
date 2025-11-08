from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.wmeta.imports import name_type_map


class MediaEntry(MemStruct):

	"""
	PC, JWE1: 32 bytes
	"""

	__name__ = 'MediaEntry'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = name_type_map['Uint'](self.context, 0, None)
		self.padding = name_type_map['Uint'].from_value(0)
		self.type_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.wav_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.wem_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'hash', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'padding', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'type_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'wav_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'wem_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'hash', name_type_map['Uint'], (0, None), (False, None)
		yield 'padding', name_type_map['Uint'], (0, None), (True, 0)
		yield 'type_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'wav_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'wem_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
