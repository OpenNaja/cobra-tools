from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.motiongraph.compound.CurveData import CurveData
from generated.formats.motiongraph.enum.TimeLimitMode import TimeLimitMode
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class DataStreamProducerActivityData(MemStruct):

	"""
	72 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.curve_type = 0
		self.curve = 0
		self.time_limit_mode = 0
		self.data_stream_producer_flags = 0
		self.ds_name = 0
		self.type = 0
		self.bone_i_d = 0
		self.location = 0
		self.prop_through_variable = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.curve_type = 0
		self.curve = CurveData(self.context, 0, None)
		self.time_limit_mode = TimeLimitMode(self.context, 0, None)
		self.data_stream_producer_flags = 0
		self.ds_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.type = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.bone_i_d = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.location = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.prop_through_variable = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.curve_type = stream.read_uint64()
		instance.ds_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.type = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.bone_i_d = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.location = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.curve = CurveData.from_stream(stream, instance.context, 0, None)
		instance.time_limit_mode = TimeLimitMode.from_value(stream.read_uint())
		instance.data_stream_producer_flags = stream.read_uint()
		instance.prop_through_variable = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.ds_name.arg = 0
		instance.type.arg = 0
		instance.bone_i_d.arg = 0
		instance.location.arg = 0
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
		stream.write_uint(instance.time_limit_mode.value)
		stream.write_uint(instance.data_stream_producer_flags)
		Pointer.to_stream(stream, instance.prop_through_variable)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('curve_type', Uint64, (0, None))
		yield ('ds_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('type', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('bone_i_d', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('location', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('curve', CurveData, (0, None))
		yield ('time_limit_mode', TimeLimitMode, (0, None))
		yield ('data_stream_producer_flags', Uint, (0, None))
		yield ('prop_through_variable', Pointer, (0, generated.formats.base.basic.ZString))

	def get_info_str(self, indent=0):
		return f'DataStreamProducerActivityData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* curve_type = {fmt_member(self.curve_type, indent+1)}'
		s += f'\n	* ds_name = {fmt_member(self.ds_name, indent+1)}'
		s += f'\n	* type = {fmt_member(self.type, indent+1)}'
		s += f'\n	* bone_i_d = {fmt_member(self.bone_i_d, indent+1)}'
		s += f'\n	* location = {fmt_member(self.location, indent+1)}'
		s += f'\n	* curve = {fmt_member(self.curve, indent+1)}'
		s += f'\n	* time_limit_mode = {fmt_member(self.time_limit_mode, indent+1)}'
		s += f'\n	* data_stream_producer_flags = {fmt_member(self.data_stream_producer_flags, indent+1)}'
		s += f'\n	* prop_through_variable = {fmt_member(self.prop_through_variable, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
