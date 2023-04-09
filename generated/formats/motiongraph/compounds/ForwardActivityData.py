from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.motiongraph.enums.UseValueType import UseValueType
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ForwardActivityData(MemStruct):

	"""
	? bytes
	"""

	__name__ = 'ForwardActivityData'

	_import_key = 'motiongraph.compounds.ForwardActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.straight_forward_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.left_forward_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.right_forward_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.straight_spot_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.forward_flags = 0
		self.suppress_resource_data_streams = 0
		self.priorities = 0
		self.turn_radius = 0.0
		self.turn_radius_value_type = UseValueType(self.context, 0, None)
		self._pad_0 = 0
		self.stride_length = 0.0
		self.stride_length_value_type = UseValueType(self.context, 0, None)
		self._pad_1 = 0
		self.lead_out_time = 0.0
		self.anticipation_distance = 0.0
		self.unfused_cycles = 0
		self.cycle_count = 0
		self.repeat_count = 0
		self.min_cycles = 0
		self.playback_rate = 0.0
		self.straight_forward_animation = Pointer(self.context, 0, ZString)
		self.left_forward_animation = Pointer(self.context, 0, ZString)
		self.right_forward_animation = Pointer(self.context, 0, ZString)
		self.straight_spot_animation = Pointer(self.context, 0, ZString)
		self.output_prop_through_variable = Pointer(self.context, 0, ZString)
		self.cycled_variable = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('straight_forward_animation', Pointer, (0, ZString), (False, None), (None, None))
		yield ('left_forward_animation', Pointer, (0, ZString), (False, None), (None, None))
		yield ('right_forward_animation', Pointer, (0, ZString), (False, None), (None, None))
		yield ('straight_spot_animation', Pointer, (0, ZString), (False, None), (None, None))
		yield ('output_prop_through_variable', Pointer, (0, ZString), (False, None), (None, None))
		yield ('cycled_variable', Pointer, (0, ZString), (False, None), (None, None))
		yield ('straight_forward_data_streams', DataStreamResourceDataList, (0, None), (False, None), (None, None))
		yield ('left_forward_data_streams', DataStreamResourceDataList, (0, None), (False, None), (None, None))
		yield ('right_forward_data_streams', DataStreamResourceDataList, (0, None), (False, None), (None, None))
		yield ('straight_spot_data_streams', DataStreamResourceDataList, (0, None), (False, None), (None, None))
		yield ('forward_flags', Ubyte, (0, None), (False, None), (None, None))
		yield ('suppress_resource_data_streams', Ubyte, (0, None), (False, None), (None, None))
		yield ('priorities', Ushort, (0, None), (False, None), (None, None))
		yield ('turn_radius', Float, (0, None), (False, None), (None, None))
		yield ('turn_radius_value_type', UseValueType, (0, None), (False, None), (None, None))
		yield ('_pad_0', Ushort, (0, None), (False, None), (None, None))
		yield ('stride_length', Float, (0, None), (False, None), (None, None))
		yield ('stride_length_value_type', UseValueType, (0, None), (False, None), (None, None))
		yield ('_pad_1', Ushort, (0, None), (False, None), (None, None))
		yield ('lead_out_time', Float, (0, None), (False, None), (None, None))
		yield ('anticipation_distance', Float, (0, None), (False, None), (None, None))
		yield ('unfused_cycles', Uint, (0, None), (False, None), (None, None))
		yield ('cycle_count', Uint, (0, None), (False, None), (None, None))
		yield ('repeat_count', Uint, (0, None), (False, None), (None, None))
		yield ('min_cycles', Uint, (0, None), (False, None), (None, None))
		yield ('playback_rate', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'straight_forward_animation', Pointer, (0, ZString), (False, None)
		yield 'left_forward_animation', Pointer, (0, ZString), (False, None)
		yield 'right_forward_animation', Pointer, (0, ZString), (False, None)
		yield 'straight_spot_animation', Pointer, (0, ZString), (False, None)
		yield 'output_prop_through_variable', Pointer, (0, ZString), (False, None)
		yield 'cycled_variable', Pointer, (0, ZString), (False, None)
		yield 'straight_forward_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'left_forward_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'right_forward_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'straight_spot_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'forward_flags', Ubyte, (0, None), (False, None)
		yield 'suppress_resource_data_streams', Ubyte, (0, None), (False, None)
		yield 'priorities', Ushort, (0, None), (False, None)
		yield 'turn_radius', Float, (0, None), (False, None)
		yield 'turn_radius_value_type', UseValueType, (0, None), (False, None)
		yield '_pad_0', Ushort, (0, None), (False, None)
		yield 'stride_length', Float, (0, None), (False, None)
		yield 'stride_length_value_type', UseValueType, (0, None), (False, None)
		yield '_pad_1', Ushort, (0, None), (False, None)
		yield 'lead_out_time', Float, (0, None), (False, None)
		yield 'anticipation_distance', Float, (0, None), (False, None)
		yield 'unfused_cycles', Uint, (0, None), (False, None)
		yield 'cycle_count', Uint, (0, None), (False, None)
		yield 'repeat_count', Uint, (0, None), (False, None)
		yield 'min_cycles', Uint, (0, None), (False, None)
		yield 'playback_rate', Float, (0, None), (False, None)
