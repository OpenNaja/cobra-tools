from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.vendingmachineinteractionsettings.imports import name_type_map


class GuestAnimationInteractionList(MemStruct):

	__name__ = 'GuestAnimationInteractionList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.type = name_type_map['Uint'](self.context, 0, None)
		self.unk_0 = name_type_map['Uint'](self.context, 0, None)
		self.interact_idle_count = name_type_map['Uint'](self.context, 0, None)
		self.unk_0 = name_type_map['Uint'](self.context, 0, None)
		self.interact_in = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.interact_loop = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.interact_out = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.interact_idle = name_type_map['Pointer'](self.context, self.interact_idle_count, name_type_map['ZStringList'])
		self.interaction_grab = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.interaction_good = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.interaction_neutral = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.interaction_bad = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.interaction_none = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'type', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'interact_in', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'interact_loop', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'interact_out', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'interact_idle', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'interact_idle_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'interaction_grab', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'interaction_good', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'interaction_neutral', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'interaction_bad', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'interaction_none', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'type', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'interact_in', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'interact_loop', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'interact_out', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'interact_idle', name_type_map['Pointer'], (instance.interact_idle_count, name_type_map['ZStringList']), (False, None)
		yield 'interact_idle_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'interaction_grab', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'interaction_good', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'interaction_neutral', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'interaction_bad', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'interaction_none', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
