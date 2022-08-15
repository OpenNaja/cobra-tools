import generated.formats.base.basic
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.motiongraph.compounds.CurveData import CurveData
from generated.formats.motiongraph.enums.TimeLimitMode import TimeLimitMode
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DataStreamProducerActivityData(MemStruct):

	"""
	72 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.curve_type = 0
		self.curve = CurveData(self.context, 0, None)
		self.time_limit_mode = TimeLimitMode(self.context, 0, None)
		self.data_stream_producer_flags = 0
		self.ds_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.type = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.bone_i_d = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.location = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.prop_through_variable = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.curve_type = 0
		self.curve = CurveData(self.context, 0, None)
		self.time_limit_mode = TimeLimitMode(self.context, 0, None)
		self.data_stream_producer_flags = 0
		self.ds_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.type = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.bone_i_d = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.location = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.prop_through_variable = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.curve_type = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ds_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.type = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.bone_i_d = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.location = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.curve = CurveData.from_stream(stream, instance.context, 0, None)
		instance.time_limit_mode = TimeLimitMode.from_stream(stream, instance.context, 0, None)
		instance.data_stream_producer_flags = Uint.from_stream(stream, instance.context, 0, None)
		instance.prop_through_variable = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
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
		stream.write_uint64(instance.curve_type)
		Pointer.to_stream(stream, instance.ds_name)
		Pointer.to_stream(stream, instance.type)
		Pointer.to_stream(stream, instance.bone_i_d)
		Pointer.to_stream(stream, instance.location)
		CurveData.to_stream(stream, instance.curve)
		TimeLimitMode.to_stream(stream, instance.time_limit_mode)
		stream.write_uint(instance.data_stream_producer_flags)
		Pointer.to_stream(stream, instance.prop_through_variable)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'curve_type', Uint64, (0, None)
		yield 'ds_name', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'type', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'bone_i_d', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'location', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'curve', CurveData, (0, None)
		yield 'time_limit_mode', TimeLimitMode, (0, None)
		yield 'data_stream_producer_flags', Uint, (0, None)
		yield 'prop_through_variable', Pointer, (0, generated.formats.base.basic.ZString)

	def get_info_str(self, indent=0):
		return f'DataStreamProducerActivityData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* curve_type = {self.fmt_member(self.curve_type, indent+1)}'
		s += f'\n	* ds_name = {self.fmt_member(self.ds_name, indent+1)}'
		s += f'\n	* type = {self.fmt_member(self.type, indent+1)}'
		s += f'\n	* bone_i_d = {self.fmt_member(self.bone_i_d, indent+1)}'
		s += f'\n	* location = {self.fmt_member(self.location, indent+1)}'
		s += f'\n	* curve = {self.fmt_member(self.curve, indent+1)}'
		s += f'\n	* time_limit_mode = {self.fmt_member(self.time_limit_mode, indent+1)}'
		s += f'\n	* data_stream_producer_flags = {self.fmt_member(self.data_stream_producer_flags, indent+1)}'
		s += f'\n	* prop_through_variable = {self.fmt_member(self.prop_through_variable, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
