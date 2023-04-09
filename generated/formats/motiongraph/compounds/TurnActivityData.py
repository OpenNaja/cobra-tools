from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.bitstructs.TurnFlags import TurnFlags
from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TurnActivityData(MemStruct):

	"""
	? bytes
	"""

	__name__ = 'TurnActivityData'

	_import_key = 'motiongraph.compounds.TurnActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.spot_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.half_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.full_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.suppress_resource_data_streams = 0
		self._pad_0 = 0
		self.priorities = 0
		self.lead_out_time = 0.0
		self.flags = TurnFlags(self.context, 0, None)
		self._pad_1 = 0
		self._pad_2 = 0
		self.max_angle = 0.0
		self.min_cycles = 0
		self.playback_rate = 0.0
		self.spot_animation = Pointer(self.context, 0, ZString)
		self.half_animation = Pointer(self.context, 0, ZString)
		self.full_animation = Pointer(self.context, 0, ZString)
		self.output_prop_through_variable = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('spot_animation', Pointer, (0, ZString), (False, None), (None, None))
		yield ('half_animation', Pointer, (0, ZString), (False, None), (None, None))
		yield ('full_animation', Pointer, (0, ZString), (False, None), (None, None))
		yield ('output_prop_through_variable', Pointer, (0, ZString), (False, None), (None, None))
		yield ('spot_data_streams', DataStreamResourceDataList, (0, None), (False, None), (None, None))
		yield ('half_data_streams', DataStreamResourceDataList, (0, None), (False, None), (None, None))
		yield ('full_data_streams', DataStreamResourceDataList, (0, None), (False, None), (None, None))
		yield ('suppress_resource_data_streams', Ubyte, (0, None), (False, None), (None, None))
		yield ('_pad_0', Ubyte, (0, None), (False, None), (None, None))
		yield ('priorities', Ushort, (0, None), (False, None), (None, None))
		yield ('lead_out_time', Float, (0, None), (False, None), (None, None))
		yield ('flags', TurnFlags, (0, None), (False, None), (None, None))
		yield ('_pad_1', Ubyte, (0, None), (False, None), (None, None))
		yield ('_pad_2', Ushort, (0, None), (False, None), (None, None))
		yield ('max_angle', Float, (0, None), (False, None), (None, None))
		yield ('min_cycles', Uint, (0, None), (False, None), (None, None))
		yield ('playback_rate', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'spot_animation', Pointer, (0, ZString), (False, None)
		yield 'half_animation', Pointer, (0, ZString), (False, None)
		yield 'full_animation', Pointer, (0, ZString), (False, None)
		yield 'output_prop_through_variable', Pointer, (0, ZString), (False, None)
		yield 'spot_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'half_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'full_data_streams', DataStreamResourceDataList, (0, None), (False, None)
		yield 'suppress_resource_data_streams', Ubyte, (0, None), (False, None)
		yield '_pad_0', Ubyte, (0, None), (False, None)
		yield 'priorities', Ushort, (0, None), (False, None)
		yield 'lead_out_time', Float, (0, None), (False, None)
		yield 'flags', TurnFlags, (0, None), (False, None)
		yield '_pad_1', Ubyte, (0, None), (False, None)
		yield '_pad_2', Ushort, (0, None), (False, None)
		yield 'max_angle', Float, (0, None), (False, None)
		yield 'min_cycles', Uint, (0, None), (False, None)
		yield 'playback_rate', Float, (0, None), (False, None)
