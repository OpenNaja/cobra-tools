from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class NodeBaseParams(BaseStruct):

	__name__ = 'NodeBaseParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.node_initial_fx_params = name_type_map['NodeInitialFxParams'](self.context, 0, None)
		self.b_is_override_parent_metadata = name_type_map['Byte'](self.context, 0, None)
		self.u_num_fx = name_type_map['Byte'](self.context, 0, None)
		self.fx = Array(self.context, 0, None, (0,), name_type_map['FXChunkBase'])
		self.b_override_attachment_params = name_type_map['Byte'](self.context, 0, None)
		self.override_bus_id = name_type_map['Uint'](self.context, 0, None)
		self.direct_parent_i_d = name_type_map['Uint'](self.context, 0, None)
		self.by_bit_vector = name_type_map['Ubyte'](self.context, 0, None)
		self.node_initial_params = name_type_map['NodeInitialParams'](self.context, 0, None)
		self.positioning_params = name_type_map['PositioningParams'](self.context, 0, None)
		self.aux_params = name_type_map['AuxParams'](self.context, 0, None)
		self.adv_settings_params = name_type_map['AdvSettingsParams'](self.context, 0, None)
		self.state_chunk = name_type_map['StateChunk'](self.context, 0, None)
		self.initial_r_t_p_c = name_type_map['InitialRTPC'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'node_initial_fx_params', name_type_map['NodeInitialFxParams'], (0, None), (False, None), (None, None)
		yield 'b_is_override_parent_metadata', name_type_map['Byte'], (0, None), (False, None), (lambda context: context.version >= 140, None)
		yield 'u_num_fx', name_type_map['Byte'], (0, None), (False, None), (lambda context: context.version >= 140, None)
		yield 'fx', Array, (0, None, (None,), name_type_map['FXChunkBase']), (False, None), (lambda context: context.version >= 140, None)
		yield 'b_override_attachment_params', name_type_map['Byte'], (0, None), (False, None), (None, None)
		yield 'override_bus_id', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'direct_parent_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'node_initial_params', name_type_map['NodeInitialParams'], (0, None), (False, None), (None, None)
		yield 'positioning_params', name_type_map['PositioningParams'], (0, None), (False, None), (None, None)
		yield 'aux_params', name_type_map['AuxParams'], (0, None), (False, None), (None, None)
		yield 'adv_settings_params', name_type_map['AdvSettingsParams'], (0, None), (False, None), (None, None)
		yield 'state_chunk', name_type_map['StateChunk'], (0, None), (False, None), (None, None)
		yield 'initial_r_t_p_c', name_type_map['InitialRTPC'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'node_initial_fx_params', name_type_map['NodeInitialFxParams'], (0, None), (False, None)
		if instance.context.version >= 140:
			yield 'b_is_override_parent_metadata', name_type_map['Byte'], (0, None), (False, None)
			yield 'u_num_fx', name_type_map['Byte'], (0, None), (False, None)
			yield 'fx', Array, (0, None, (instance.u_num_fx,), name_type_map['FXChunkBase']), (False, None)
		yield 'b_override_attachment_params', name_type_map['Byte'], (0, None), (False, None)
		yield 'override_bus_id', name_type_map['Uint'], (0, None), (False, None)
		yield 'direct_parent_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'node_initial_params', name_type_map['NodeInitialParams'], (0, None), (False, None)
		yield 'positioning_params', name_type_map['PositioningParams'], (0, None), (False, None)
		yield 'aux_params', name_type_map['AuxParams'], (0, None), (False, None)
		yield 'adv_settings_params', name_type_map['AdvSettingsParams'], (0, None), (False, None)
		yield 'state_chunk', name_type_map['StateChunk'], (0, None), (False, None)
		yield 'initial_r_t_p_c', name_type_map['InitialRTPC'], (0, None), (False, None)
