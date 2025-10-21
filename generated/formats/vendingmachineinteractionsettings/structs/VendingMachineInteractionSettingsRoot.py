from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.vendingmachineinteractionsettings.imports import name_type_map


class VendingMachineInteractionSettingsRoot(MemStruct):

	"""
	PC 80 bytes
	"""

	__name__ = 'VendingMachineInteractionSettingsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.animation_interaction_count = name_type_map['Uint'](self.context, 0, None)
		self.float_1 = name_type_map['Float'].from_value(9.0)
		self.float_2 = name_type_map['Float'].from_value(12.0)
		self.unk_1 = name_type_map['Uint'](self.context, 0, None)
		self.animation_idle_count = name_type_map['Uint'](self.context, 0, None)
		self.unk_2 = name_type_map['Uint'](self.context, 0, None)
		self.animation_win_count = name_type_map['Uint'](self.context, 0, None)
		self.unk_3 = name_type_map['Uint'](self.context, 0, None)
		self.animation_fail_count = name_type_map['Uint'](self.context, 0, None)
		self.float_3 = name_type_map['Float'].from_value(12.0)
		self.pad_0 = name_type_map['Uint'](self.context, 0, None)
		self.pad_1 = name_type_map['Uint'](self.context, 0, None)
		self.animation_interaction = name_type_map['ArrayPointer'](self.context, self.animation_interaction_count, name_type_map['GuestAnimationInteractionList'])
		self.animation_idle = name_type_map['Pointer'](self.context, self.animation_idle_count, name_type_map['ZStringList'])
		self.animation_win = name_type_map['Pointer'](self.context, self.animation_win_count, name_type_map['ZStringList'])
		self.animation_fail = name_type_map['Pointer'](self.context, self.animation_fail_count, name_type_map['ZStringList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'animation_interaction', name_type_map['ArrayPointer'], (None, name_type_map['GuestAnimationInteractionList']), (False, None), (None, None)
		yield 'animation_interaction_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'float_1', name_type_map['Float'], (0, None), (False, 9.0), (None, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, 12.0), (None, None)
		yield 'unk_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'animation_idle', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'animation_idle_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'animation_win', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'animation_win_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'animation_fail', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'animation_fail_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, 12.0), (None, None)
		yield 'pad_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'pad_1', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'animation_interaction', name_type_map['ArrayPointer'], (instance.animation_interaction_count, name_type_map['GuestAnimationInteractionList']), (False, None)
		yield 'animation_interaction_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'float_1', name_type_map['Float'], (0, None), (False, 9.0)
		yield 'float_2', name_type_map['Float'], (0, None), (False, 12.0)
		yield 'unk_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'animation_idle', name_type_map['Pointer'], (instance.animation_idle_count, name_type_map['ZStringList']), (False, None)
		yield 'animation_idle_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'animation_win', name_type_map['Pointer'], (instance.animation_win_count, name_type_map['ZStringList']), (False, None)
		yield 'animation_win_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'animation_fail', name_type_map['Pointer'], (instance.animation_fail_count, name_type_map['ZStringList']), (False, None)
		yield 'animation_fail_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, 12.0)
		yield 'pad_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'pad_1', name_type_map['Uint'], (0, None), (False, None)
