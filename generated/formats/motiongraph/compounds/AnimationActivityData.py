from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.bitstructs.AnimationFlags import AnimationFlags
from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.motiongraph.compounds.FloatInputData import FloatInputData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AnimationActivityData(MemStruct):

	"""
	96 bytes
	"""

	__name__ = 'AnimationActivityData'

	_import_key = 'motiongraph.compounds.AnimationActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.animation_flags = AnimationFlags(self.context, 0, None)
		self.priorities = 0
		self.weight = FloatInputData(self.context, 0, None)
		self.speed = FloatInputData(self.context, 0, None)
		self.starting_prop_through = 0.0
		self.lead_out_time = 0.0
		self.count_6 = 0
		self.additional_data_streams = DataStreamResourceDataList(self.context, 0, None)
		self.mani = Pointer(self.context, 0, ZString)
		self.sync_prop_through_variable = Pointer(self.context, 0, ZString)
		self.output_prop_through_variable = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('mani', Pointer, (0, ZString), (False, None), None),
		('animation_flags', AnimationFlags, (0, None), (False, None), None),
		('priorities', Uint, (0, None), (False, None), None),
		('weight', FloatInputData, (0, None), (False, None), None),
		('speed', FloatInputData, (0, None), (False, None), None),
		('starting_prop_through', Float, (0, None), (False, None), None),
		('lead_out_time', Float, (0, None), (False, None), None),
		('sync_prop_through_variable', Pointer, (0, ZString), (False, None), None),
		('count_6', Uint64, (0, None), (False, None), None),
		('output_prop_through_variable', Pointer, (0, ZString), (False, None), None),
		('additional_data_streams', DataStreamResourceDataList, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'mani', Pointer, (0, ZString), (False, None)
		yield 'animation_flags', AnimationFlags, (0, None), (False, None)
		yield 'priorities', Uint, (0, None), (False, None)
		yield 'weight', FloatInputData, (0, None), (False, None)
		yield 'speed', FloatInputData, (0, None), (False, None)
		yield 'starting_prop_through', Float, (0, None), (False, None)
		yield 'lead_out_time', Float, (0, None), (False, None)
		yield 'sync_prop_through_variable', Pointer, (0, ZString), (False, None)
		yield 'count_6', Uint64, (0, None), (False, None)
		yield 'output_prop_through_variable', Pointer, (0, ZString), (False, None)
		yield 'additional_data_streams', DataStreamResourceDataList, (0, None), (False, None)
