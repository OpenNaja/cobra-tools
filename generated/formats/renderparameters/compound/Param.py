from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.renderparameters.compound.ParamData import ParamData
from generated.formats.renderparameters.enum.RenderParameterType import RenderParameterType


class Param(MemStruct):

	"""
	32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.dtype = 0
		self.data = 0
		self.attribute_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.dtype = RenderParameterType(self.context, 0, None)
		self.data = ParamData(self.context, self.dtype, None)
		self.attribute_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.attribute_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.dtype = RenderParameterType.from_value(stream.read_uint64())
		instance.data = ParamData.from_stream(stream, instance.context, instance.dtype, None)
		instance.attribute_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attribute_name)
		stream.write_uint64(instance.dtype.value)
		ParamData.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('attribute_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('dtype', RenderParameterType, (0, None))
		yield ('data', ParamData, (instance.dtype, None))

	def get_info_str(self, indent=0):
		return f'Param [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* attribute_name = {fmt_member(self.attribute_name, indent+1)}'
		s += f'\n	* dtype = {fmt_member(self.dtype, indent+1)}'
		s += f'\n	* data = {fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
