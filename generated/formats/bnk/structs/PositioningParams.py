from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class PositioningParams(BaseStruct):

	__name__ = 'PositioningParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_bits_positioning = name_type_map['UBitsPositioning'](self.context, 0, None)
		self.u_bits_3_d = name_type_map['Ubyte'](self.context, 0, None)
		self.u_attenuation_i_d = name_type_map['Int'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'u_bits_positioning', name_type_map['UBitsPositioning122'], (0, None), (False, None), (lambda context: context.version <= 122, None)
		yield 'u_bits_positioning', name_type_map['UBitsPositioning'], (0, None), (False, None), (lambda context: context.version >= 130, None)
		yield 'u_bits_3_d', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version >= 130, True)
		yield 'u_bits_3_d', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version <= 122, True)
		yield 'positioning_automation', name_type_map['PositioningAutomation'], (0, None), (False, None), (lambda context: context.version >= 130, True)
		yield 'u_attenuation_i_d', name_type_map['Int'], (0, None), (False, None), (lambda context: context.version <= 129, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 122:
			yield 'u_bits_positioning', name_type_map['UBitsPositioning122'], (0, None), (False, None)
		if instance.context.version >= 130:
			yield 'u_bits_positioning', name_type_map['UBitsPositioning'], (0, None), (False, None)
		if instance.context.version >= 130 and instance.u_bits_positioning.b_positioning_info_override_parent and instance.u_bits_positioning.b_has_listener_relative_routing:
			yield 'u_bits_3_d', name_type_map['Ubyte'], (0, None), (False, None)
		if instance.context.version <= 122 and instance.u_bits_positioning.b_positioning_info_override_parent and instance.u_bits_positioning.cb_is_3_d_positioning_available:
			yield 'u_bits_3_d', name_type_map['Ubyte'], (0, None), (False, None)
		if instance.context.version >= 130 and instance.u_bits_positioning.e_3_d_position_type and (instance.u_bits_positioning.b_positioning_info_override_parent and instance.u_bits_positioning.b_has_listener_relative_routing):
			yield 'positioning_automation', name_type_map['PositioningAutomation'], (0, None), (False, None)
		if instance.context.version <= 129 and instance.u_bits_positioning.b_positioning_info_override_parent and instance.u_bits_positioning.cb_is_3_d_positioning_available:
			yield 'u_attenuation_i_d', name_type_map['Int'], (0, None), (False, None)
