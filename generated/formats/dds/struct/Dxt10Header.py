from generated.base_struct import BaseStruct
from generated.formats.dds.basic import Uint
from generated.formats.dds.enums.D3D10ResourceDimension import D3D10ResourceDimension
from generated.formats.dds.enums.DxgiFormat import DxgiFormat


class Dxt10Header(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dxgi_format = 0
		self.resource_dimension = 0
		self.misc_flag = 0
		self.array_size = 0
		self.misc_flag_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.dxgi_format = DxgiFormat(self.context, 0, None)
		self.resource_dimension = D3D10ResourceDimension(self.context, 0, None)
		self.misc_flag = 0
		self.array_size = 0
		self.misc_flag_2 = 0

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
		instance.dxgi_format = DxgiFormat.from_stream(stream, instance.context, 0, None)
		instance.resource_dimension = D3D10ResourceDimension.from_stream(stream, instance.context, 0, None)
		instance.misc_flag = stream.read_uint()
		instance.array_size = stream.read_uint()
		instance.misc_flag_2 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		DxgiFormat.to_stream(stream, instance.dxgi_format)
		D3D10ResourceDimension.to_stream(stream, instance.resource_dimension)
		stream.write_uint(instance.misc_flag)
		stream.write_uint(instance.array_size)
		stream.write_uint(instance.misc_flag_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('dxgi_format', DxgiFormat, (0, None))
		yield ('resource_dimension', D3D10ResourceDimension, (0, None))
		yield ('misc_flag', Uint, (0, None))
		yield ('array_size', Uint, (0, None))
		yield ('misc_flag_2', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'Dxt10Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* dxgi_format = {self.fmt_member(self.dxgi_format, indent+1)}'
		s += f'\n	* resource_dimension = {self.fmt_member(self.resource_dimension, indent+1)}'
		s += f'\n	* misc_flag = {self.fmt_member(self.misc_flag, indent+1)}'
		s += f'\n	* array_size = {self.fmt_member(self.array_size, indent+1)}'
		s += f'\n	* misc_flag_2 = {self.fmt_member(self.misc_flag_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
