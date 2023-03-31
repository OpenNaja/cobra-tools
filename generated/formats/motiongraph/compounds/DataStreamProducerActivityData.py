from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.compounds.CurveData import CurveData
from generated.formats.motiongraph.enums.TimeLimitMode import TimeLimitMode
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DataStreamProducerActivityData(MemStruct):

	"""
	72 bytes
	"""

	__name__ = 'DataStreamProducerActivityData'

	_import_key = 'motiongraph.compounds.DataStreamProducerActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.curve_type = 0
		self.curve = CurveData(self.context, 0, None)
		self.time_limit_mode = TimeLimitMode(self.context, 0, None)
		self.data_stream_producer_flags = 0
		self.ds_name = Pointer(self.context, 0, ZString)
		self.type = Pointer(self.context, 0, ZString)
		self.bone_i_d = Pointer(self.context, 0, ZString)
		self.location = Pointer(self.context, 0, ZString)
		self.prop_through_variable = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('curve_type', Uint64, (0, None), (False, None), None)
		yield ('ds_name', Pointer, (0, ZString), (False, None), None)
		yield ('type', Pointer, (0, ZString), (False, None), None)
		yield ('bone_i_d', Pointer, (0, ZString), (False, None), None)
		yield ('location', Pointer, (0, ZString), (False, None), None)
		yield ('curve', CurveData, (0, None), (False, None), None)
		yield ('time_limit_mode', TimeLimitMode, (0, None), (False, None), None)
		yield ('data_stream_producer_flags', Uint, (0, None), (False, None), None)
		yield ('prop_through_variable', Pointer, (0, ZString), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'curve_type', Uint64, (0, None), (False, None)
		yield 'ds_name', Pointer, (0, ZString), (False, None)
		yield 'type', Pointer, (0, ZString), (False, None)
		yield 'bone_i_d', Pointer, (0, ZString), (False, None)
		yield 'location', Pointer, (0, ZString), (False, None)
		yield 'curve', CurveData, (0, None), (False, None)
		yield 'time_limit_mode', TimeLimitMode, (0, None), (False, None)
		yield 'data_stream_producer_flags', Uint, (0, None), (False, None)
		yield 'prop_through_variable', Pointer, (0, ZString), (False, None)


DataStreamProducerActivityData.init_attributes()
