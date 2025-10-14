from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class PositioningParams(BaseStruct):

	__name__ = 'PositioningParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_bits_positioning = name_type_map['UBitsPositioning'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'u_bits_positioning', name_type_map['UBitsPositioning'], (0, None), (False, None), (None, None)
		yield 'positioning_data', name_type_map['PositioningData'], (0, None), (False, None), (None, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_bits_positioning', name_type_map['UBitsPositioning'], (0, None), (False, None)
		if instance.u_bits_positioning.b_positioning_info_override_parent and instance.u_bits_positioning.b_has_listener_relative_routing:
			yield 'positioning_data', name_type_map['PositioningData'], (0, None), (False, None)
