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

	_import_path = 'generated.formats.motiongraph.compounds.DataStreamProducerActivityData'

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

	def set_defaults(self):
		super().set_defaults()
		self.curve_type = 0
		self.curve = CurveData(self.context, 0, None)
		self.time_limit_mode = TimeLimitMode(self.context, 0, None)
		self.data_stream_producer_flags = 0
		self.ds_name = Pointer(self.context, 0, ZString)
		self.type = Pointer(self.context, 0, ZString)
		self.bone_i_d = Pointer(self.context, 0, ZString)
		self.location = Pointer(self.context, 0, ZString)
		self.prop_through_variable = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.curve_type = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ds_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.type = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.bone_i_d = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.location = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.curve = CurveData.from_stream(stream, instance.context, 0, None)
		instance.time_limit_mode = TimeLimitMode.from_stream(stream, instance.context, 0, None)
		instance.data_stream_producer_flags = Uint.from_stream(stream, instance.context, 0, None)
		instance.prop_through_variable = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.ds_name, int):
			instance.ds_name.arg = 0
		if not isinstance(instance.type, int):
			instance.type.arg = 0
		if not isinstance(instance.bone_i_d, int):
			instance.bone_i_d.arg = 0
		if not isinstance(instance.location, int):
			instance.location.arg = 0
		if not isinstance(instance.prop_through_variable, int):
			instance.prop_through_variable.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.curve_type)
		Pointer.to_stream(stream, instance.ds_name)
		Pointer.to_stream(stream, instance.type)
		Pointer.to_stream(stream, instance.bone_i_d)
		Pointer.to_stream(stream, instance.location)
		CurveData.to_stream(stream, instance.curve)
		TimeLimitMode.to_stream(stream, instance.time_limit_mode)
		Uint.to_stream(stream, instance.data_stream_producer_flags)
		Pointer.to_stream(stream, instance.prop_through_variable)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'curve_type', Uint64, (0, None), (False, None)
		yield 'ds_name', Pointer, (0, ZString), (False, None)
		yield 'type', Pointer, (0, ZString), (False, None)
		yield 'bone_i_d', Pointer, (0, ZString), (False, None)
		yield 'location', Pointer, (0, ZString), (False, None)
		yield 'curve', CurveData, (0, None), (False, None)
		yield 'time_limit_mode', TimeLimitMode, (0, None), (False, None)
		yield 'data_stream_producer_flags', Uint, (0, None), (False, None)
		yield 'prop_through_variable', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'DataStreamProducerActivityData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
