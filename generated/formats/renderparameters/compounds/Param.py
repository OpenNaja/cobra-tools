import generated.formats.base.basic
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.renderparameters.compounds.ParamData import ParamData
from generated.formats.renderparameters.enums.RenderParameterType import RenderParameterType


class Param(MemStruct):

	"""
	32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = 0
		self.data = 0
		self.attribute_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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
		instance.dtype = RenderParameterType.from_stream(stream, instance.context, 0, None)
		instance.data = ParamData.from_stream(stream, instance.context, instance.dtype, None)
		if not isinstance(instance.attribute_name, int):
			instance.attribute_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attribute_name)
		RenderParameterType.to_stream(stream, instance.dtype)
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
		s += f'\n	* attribute_name = {self.fmt_member(self.attribute_name, indent+1)}'
		s += f'\n	* dtype = {self.fmt_member(self.dtype, indent+1)}'
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
