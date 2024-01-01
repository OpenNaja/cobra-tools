from generated.array import Array
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.imports import name_type_map


class SoundSfxVoice(HircObject):

	__name__ = 'SoundSfxVoice'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# four unknown bytes
		self.const_a = name_type_map['Uint'](self.context, 0, None)

		# whether the sound is included in the SoundBank or streamed
		self.source = name_type_map['StreamSource'](self.context, 0, None)

		# ?
		self.didx_id = name_type_map['Uint'](self.context, 0, None)

		# ?
		self.wem_length = name_type_map['Uint'](self.context, 0, None)

		# ?
		self.zero = name_type_map['Uint64'](self.context, 0, None)

		# ?
		self.some_id = name_type_map['Uint'](self.context, 0, None)

		# ?
		self.zero_2 = name_type_map['Ubyte'](self.context, 0, None)

		# ?
		self.some_count = name_type_map['Ubyte'](self.context, 0, None)

		# ?
		self.some_types = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])

		# ?
		self.some_values = Array(self.context, 0, None, (0,), name_type_map['Uint'])

		# ?
		self.other_flag = name_type_map['Ubyte'](self.context, 0, None)

		# ?
		self.extra = Array(self.context, 0, None, (0,), name_type_map['Byte'])

		# ?
		self.zeros_3 = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])

		# ?
		self.rest = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'const_a', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'source', name_type_map['StreamSource'], (0, None), (False, None), (None, None)
		yield 'didx_id', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'wem_length', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'some_id', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zero_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'some_count', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'some_types', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'some_values', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'other_flag', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'extra', Array, (0, None, (None,), name_type_map['Byte']), (False, None), (None, None)
		yield 'zeros_3', Array, (0, None, (7,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'rest', Array, (0, None, (9,), name_type_map['Ubyte']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'const_a', name_type_map['Uint'], (0, None), (False, None)
		yield 'source', name_type_map['StreamSource'], (0, None), (False, None)
		yield 'didx_id', name_type_map['Uint'], (0, None), (False, None)
		yield 'wem_length', name_type_map['Uint'], (0, None), (False, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (False, None)
		yield 'some_id', name_type_map['Uint'], (0, None), (False, None)
		yield 'zero_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'some_count', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'some_types', Array, (0, None, (instance.some_count,), name_type_map['Ubyte']), (False, None)
		yield 'some_values', Array, (0, None, (instance.some_count,), name_type_map['Uint']), (False, None)
		yield 'other_flag', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'extra', Array, (0, None, (instance.length - (48 + (instance.some_count * 5)),), name_type_map['Byte']), (False, None)
		yield 'zeros_3', Array, (0, None, (7,), name_type_map['Ubyte']), (False, None)
		yield 'rest', Array, (0, None, (9,), name_type_map['Ubyte']), (False, None)
