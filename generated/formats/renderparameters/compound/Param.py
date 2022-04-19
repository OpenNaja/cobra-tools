from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.renderparameters.enum.RenderParameterType import RenderParameterType


class Param(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.dtype = RenderParameterType(self.context, 0, None)
		self.data_0 = 0.0
		self.data_1 = 0.0
		self.data_2 = 0.0
		self.data_3 = 0.0
		self.attribute_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.dtype = RenderParameterType(self.context, 0, None)
		self.data_0 = 0.0
		self.data_1 = 0.0
		self.data_2 = 0.0
		self.data_3 = 0.0
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
		instance.data_0 = stream.read_float()
		instance.data_1 = stream.read_float()
		instance.data_2 = stream.read_float()
		instance.data_3 = stream.read_float()
		instance.attribute_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attribute_name)
		stream.write_uint64(instance.dtype.value)
		stream.write_float(instance.data_0)
		stream.write_float(instance.data_1)
		stream.write_float(instance.data_2)
		stream.write_float(instance.data_3)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'Param [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* attribute_name = {fmt_member(self.attribute_name, indent+1)}'
		s += f'\n	* dtype = {fmt_member(self.dtype, indent+1)}'
		s += f'\n	* data_0 = {fmt_member(self.data_0, indent+1)}'
		s += f'\n	* data_1 = {fmt_member(self.data_1, indent+1)}'
		s += f'\n	* data_2 = {fmt_member(self.data_2, indent+1)}'
		s += f'\n	* data_3 = {fmt_member(self.data_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
