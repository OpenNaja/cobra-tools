from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class StateChunk(BaseStruct):

	__name__ = 'StateChunk'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ul_num_state_props = name_type_map['Ubyte'](self.context, 0, None)
		self.state_props = Array(self.context, 0, None, (0,), name_type_map['AkStatePropertyInfo'])
		self.ul_num_state_groups = name_type_map['Ubyte'](self.context, 0, None)
		self.state_groups = Array(self.context, 0, None, (0,), name_type_map['AkStateGroupChunk'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ul_num_state_props', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'state_props', Array, (0, None, (None,), name_type_map['AkStatePropertyInfo']), (False, None), (None, None)
		yield 'ul_num_state_groups', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'state_groups', Array, (0, None, (None,), name_type_map['AkStateGroupChunk']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ul_num_state_props', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'state_props', Array, (0, None, (instance.ul_num_state_props,), name_type_map['AkStatePropertyInfo']), (False, None)
		yield 'ul_num_state_groups', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'state_groups', Array, (0, None, (instance.ul_num_state_groups,), name_type_map['AkStateGroupChunk']), (False, None)
