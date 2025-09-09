from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class NodeInitialFxParams(BaseStruct):

	__name__ = 'NodeInitialFxParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.b_is_override_parent_f_x = name_type_map['Byte'](self.context, 0, None)
		self.u_num_fx = name_type_map['Byte'](self.context, 0, None)
		self.bits_f_x_bypass = name_type_map['Byte'](self.context, 0, None)
		self.fx = Array(self.context, 0, None, (0,), name_type_map['FXChunk'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'b_is_override_parent_f_x', name_type_map['Byte'], (0, None), (False, None), (None, None)
		yield 'u_num_fx', name_type_map['Byte'], (0, None), (False, None), (None, None)
		yield 'bits_f_x_bypass', name_type_map['Byte'], (0, None), (False, None), (None, True)
		yield 'fx', Array, (0, None, (None,), name_type_map['FXChunk']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'b_is_override_parent_f_x', name_type_map['Byte'], (0, None), (False, None)
		yield 'u_num_fx', name_type_map['Byte'], (0, None), (False, None)
		if instance.u_num_fx:
			yield 'bits_f_x_bypass', name_type_map['Byte'], (0, None), (False, None)
		yield 'fx', Array, (0, None, (instance.u_num_fx,), name_type_map['FXChunk']), (False, None)
