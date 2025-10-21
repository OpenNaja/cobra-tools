from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class BKHDSection(BaseStruct):

	__name__ = 'BKHDSection'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of following data
		self.length = name_type_map['Uint'](self.context, 0, None)
		self.version = name_type_map['Uint'](self.context, 0, None)
		self.dw_sound_bank_i_d = name_type_map['Uint'](self.context, 0, None)
		self.dw_language_i_d = name_type_map['Uint'](self.context, 0, None)
		self.u_alignment = name_type_map['Ushort'](self.context, 0, None)
		self.b_device_allocated = name_type_map['Ushort'](self.context, 0, None)
		self.dw_project_i_d = name_type_map['Uint'](self.context, 0, None)

		# sometimes present
		self.padding = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'length', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'version', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'dw_sound_bank_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'dw_language_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'u_alignment', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'b_device_allocated', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'dw_project_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'padding', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', name_type_map['Uint'], (0, None), (False, None)
		yield 'version', name_type_map['Uint'], (0, None), (False, None)
		yield 'dw_sound_bank_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'dw_language_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'u_alignment', name_type_map['Ushort'], (0, None), (False, None)
		yield 'b_device_allocated', name_type_map['Ushort'], (0, None), (False, None)
		yield 'dw_project_i_d', name_type_map['Uint'], (0, None), (False, None)
		if instance.length >= 20:
			yield 'padding', Array, (0, None, (instance.length - 20,), name_type_map['Ubyte']), (False, None)
