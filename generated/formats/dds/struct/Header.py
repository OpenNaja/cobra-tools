import typing
from generated.array import Array
from generated.formats.dds.bitstruct.Caps1 import Caps1
from generated.formats.dds.bitstruct.Caps2 import Caps2
from generated.formats.dds.bitstruct.HeaderFlags import HeaderFlags
from generated.formats.dds.compound.FixedString import FixedString
from generated.formats.dds.struct.Dxt10Header import Dxt10Header
from generated.formats.dds.struct.PixelFormat import PixelFormat


class Header:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# DDS
		self.header_string = FixedString()

		# Always 124 + 4 bytes for headerstring, header ends at 128.
		self.size = 124
		self.flags = HeaderFlags()

		# The texture height.
		self.height = 0

		# The texture width.
		self.width = 0
		self.linear_size = 0
		self.depth = 0
		self.mipmap_count = 0
		self.reserved_1 = Array()
		self.pixel_format = PixelFormat()
		self.caps_1 = Caps1()
		self.caps_2 = Caps2()
		self.caps_3 = 0
		self.caps_4 = 0
		self.unused = 0
		self.dx_10 = Dxt10Header()

	def read(self, stream):

		self.io_start = stream.tell()
		self.header_string = stream.read_type(FixedString, (4,))
		self.size = stream.read_uint()
		self.flags = stream.read_type(HeaderFlags)
		self.height = stream.read_uint()
		self.width = stream.read_uint()
		self.linear_size = stream.read_uint()
		self.depth = stream.read_uint()
		self.mipmap_count = stream.read_uint()
		self.reserved_1.read(stream, 'Uint', 11, None)
		self.pixel_format = stream.read_type(PixelFormat)
		self.caps_1 = stream.read_type(Caps1)
		self.caps_2 = stream.read_type(Caps2)
		self.caps_3 = stream.read_uint()
		self.caps_4 = stream.read_uint()
		self.unused = stream.read_uint()
		if self.pixel_format.four_c_c == 808540228:
			self.dx_10 = stream.read_type(Dxt10Header)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.header_string)
		stream.write_uint(self.size)
		stream.write_type(self.flags)
		stream.write_uint(self.height)
		stream.write_uint(self.width)
		stream.write_uint(self.linear_size)
		stream.write_uint(self.depth)
		stream.write_uint(self.mipmap_count)
		self.reserved_1.write(stream, 'Uint', 11, None)
		stream.write_type(self.pixel_format)
		stream.write_type(self.caps_1)
		stream.write_type(self.caps_2)
		stream.write_uint(self.caps_3)
		stream.write_uint(self.caps_4)
		stream.write_uint(self.unused)
		if self.pixel_format.four_c_c == 808540228:
			stream.write_type(self.dx_10)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Header [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* header_string = ' + self.header_string.__repr__()
		s += '\n	* size = ' + self.size.__repr__()
		s += '\n	* flags = ' + self.flags.__repr__()
		s += '\n	* height = ' + self.height.__repr__()
		s += '\n	* width = ' + self.width.__repr__()
		s += '\n	* linear_size = ' + self.linear_size.__repr__()
		s += '\n	* depth = ' + self.depth.__repr__()
		s += '\n	* mipmap_count = ' + self.mipmap_count.__repr__()
		s += '\n	* reserved_1 = ' + self.reserved_1.__repr__()
		s += '\n	* pixel_format = ' + self.pixel_format.__repr__()
		s += '\n	* caps_1 = ' + self.caps_1.__repr__()
		s += '\n	* caps_2 = ' + self.caps_2.__repr__()
		s += '\n	* caps_3 = ' + self.caps_3.__repr__()
		s += '\n	* caps_4 = ' + self.caps_4.__repr__()
		s += '\n	* unused = ' + self.unused.__repr__()
		s += '\n	* dx_10 = ' + self.dx_10.__repr__()
		s += '\n'
		return s
