from generated.context import ContextReference
from generated.formats.dds.enum.D3D10ResourceDimension import D3D10ResourceDimension
from generated.formats.dds.enum.DxgiFormat import DxgiFormat


class Dxt10Header:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.dxgi_format = DxgiFormat()
		self.resource_dimension = D3D10ResourceDimension()
		self.misc_flag = 0
		self.array_size = 0
		self.misc_flag_2 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.dxgi_format = DxgiFormat(stream.read_uint())
		self.resource_dimension = D3D10ResourceDimension(stream.read_uint())
		self.misc_flag = stream.read_uint()
		self.array_size = stream.read_uint()
		self.misc_flag_2 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.dxgi_format.value)
		stream.write_uint(self.resource_dimension.value)
		stream.write_uint(self.misc_flag)
		stream.write_uint(self.array_size)
		stream.write_uint(self.misc_flag_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Dxt10Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* dxgi_format = {self.dxgi_format.__repr__()}'
		s += f'\n	* resource_dimension = {self.resource_dimension.__repr__()}'
		s += f'\n	* misc_flag = {self.misc_flag.__repr__()}'
		s += f'\n	* array_size = {self.array_size.__repr__()}'
		s += f'\n	* misc_flag_2 = {self.misc_flag_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
