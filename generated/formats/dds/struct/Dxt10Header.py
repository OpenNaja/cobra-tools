from generated.formats.dds.enum.DxgiFormat import DxgiFormat
from generated.formats.dds.enum.D3D10ResourceDimension import D3D10ResourceDimension


class Dxt10Header:
	dxgi_format: DxgiFormat
	resource_dimension: D3D10ResourceDimension
	misc_flag: int
	array_size: int
	misc_flag_2: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.dxgi_format = 0
		self.resource_dimension = 0
		self.misc_flag = 0
		self.array_size = 0
		self.misc_flag_2 = 0

	def read(self, stream):

		io_start = stream.tell()
		self.dxgi_format = stream.read_type(DxgiFormat)
		self.resource_dimension = stream.read_type(D3D10ResourceDimension)
		self.misc_flag = stream.read_uint()
		self.array_size = stream.read_uint()
		self.misc_flag_2 = stream.read_uint()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_type(self.dxgi_format)
		stream.write_type(self.resource_dimension)
		stream.write_uint(self.misc_flag)
		stream.write_uint(self.array_size)
		stream.write_uint(self.misc_flag_2)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'Dxt10Header [Size: '+str(self.io_size)+']'
		s += '\n	* dxgi_format = ' + self.dxgi_format.__repr__()
		s += '\n	* resource_dimension = ' + self.resource_dimension.__repr__()
		s += '\n	* misc_flag = ' + self.misc_flag.__repr__()
		s += '\n	* array_size = ' + self.array_size.__repr__()
		s += '\n	* misc_flag_2 = ' + self.misc_flag_2.__repr__()
		s += '\n'
		return s
