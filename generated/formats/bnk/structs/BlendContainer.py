from generated.array import Array
from generated.formats.bnk.imports import name_type_map
from generated.formats.bnk.structs.HircObject import HircObject


class BlendContainer(HircObject):

	__name__ = 'BlendContainer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.node_base_params = name_type_map['NodeBaseParams'](self.context, 0, None)
		self.num_children = name_type_map['Uint'](self.context, 0, None)
		self.children = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.ul_num_layers = name_type_map['Uint'](self.context, 0, None)
		self.layers = Array(self.context, 0, None, (0,), name_type_map['CAkLayer'])
		self.b_is_continuous_validation = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None), (None, None)
		yield 'num_children', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'children', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'ul_num_layers', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'layers', Array, (0, None, (None,), name_type_map['CAkLayer']), (False, None), (None, None)
		yield 'b_is_continuous_validation', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None)
		yield 'num_children', name_type_map['Uint'], (0, None), (False, None)
		yield 'children', Array, (0, None, (instance.num_children,), name_type_map['Uint']), (False, None)
		yield 'ul_num_layers', name_type_map['Uint'], (0, None), (False, None)
		yield 'layers', Array, (0, None, (instance.ul_num_layers,), name_type_map['CAkLayer']), (False, None)
		yield 'b_is_continuous_validation', name_type_map['Ubyte'], (0, None), (False, None)
