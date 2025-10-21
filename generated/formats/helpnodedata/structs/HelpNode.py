from generated.formats.helpnodedata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class HelpNode(MemStruct):

	__name__ = 'HelpNode'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.node_type = name_type_map['Uint64'](self.context, 0, None)
		self.node_help_user_interface_icon_data = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.node_title_text_symbol = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.node_description_text_symbol = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_ptr_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_ptr_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_ptr_3 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_ptr_4 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_ptr_5 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_ptr_6 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'node_type', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'node_help_user_interface_icon_data', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'node_title_text_symbol', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'node_description_text_symbol', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_ptr_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_ptr_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_ptr_3', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_ptr_4', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_ptr_5', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_ptr_6', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'node_type', name_type_map['Uint64'], (0, None), (False, None)
		yield 'node_help_user_interface_icon_data', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'node_title_text_symbol', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'node_description_text_symbol', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_ptr_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_ptr_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_ptr_3', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_ptr_4', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_ptr_5', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_ptr_6', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
