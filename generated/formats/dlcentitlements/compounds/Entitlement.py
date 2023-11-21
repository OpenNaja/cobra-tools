from generated.formats.dlcentitlements.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Entitlement(MemStruct):

	__name__ = 'Entitlement'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.id = name_type_map['Uint64'](self.context, 0, None)
		self.reward_count = name_type_map['Uint64'](self.context, 0, None)
		self.entitlement_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.reward_list = name_type_map['Pointer'](self.context, self.reward_count, name_type_map['ZStringList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'entitlement_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'id', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'reward_list', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'reward_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'entitlement_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'id', name_type_map['Uint64'], (0, None), (False, None)
		yield 'reward_list', name_type_map['Pointer'], (instance.reward_count, name_type_map['ZStringList']), (False, None)
		yield 'reward_count', name_type_map['Uint64'], (0, None), (False, None)
