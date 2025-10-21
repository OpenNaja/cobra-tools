from generated.formats.helpnodedata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class HelpNodeDataHeader(MemStruct):

	__name__ = 'HelpNodeDataHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.parent_type = name_type_map['Uint64'](self.context, 0, None)
		self.node_count = name_type_map['Uint64'](self.context, 0, None)
		self.parent_node = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.nodes = name_type_map['ArrayPointer'](self.context, self.node_count, name_type_map['HelpNode'])
		self.ptr_0 = name_type_map['Pointer'](self.context, 0, None)
		self.ptr_1 = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'parent_node', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'parent_type', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'node_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'nodes', name_type_map['ArrayPointer'], (None, name_type_map['HelpNode']), (False, None), (None, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'parent_node', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'parent_type', name_type_map['Uint64'], (0, None), (False, None)
		yield 'node_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'nodes', name_type_map['ArrayPointer'], (instance.node_count, name_type_map['HelpNode']), (False, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, None), (False, None)
		yield 'ptr_1', name_type_map['Pointer'], (0, None), (False, None)
