from generated.formats.ovl.bitfield.VersionInfo import VersionInfo
from generated.formats.ovl.compound.FixedString import FixedString


class GenericHeader:

	"""
	Found at the beginning of every OVL file
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FRES'
		self.fres = FixedString()

		# if 0x08 then 64bit, 0x01 for JWE, PZ, 0x08 for PC, 0x48 for JWE Switch, may be platform
		self.version_flag = 0

		# 0x12 = PC, 0x13 = JWE, PZ
		self.version = 0

		# endianness?, usually zero
		self.bitswap = 0

		# always = 1
		self.seventh_byte = 1

		# determines compression format (none, zlib or oodle) and apparently type of data (additional fields)
		self.user_version = VersionInfo()

	def read(self, stream):

		self.io_start = stream.tell()
		self.fres = stream.read_type(FixedString, (4,))
		self.version_flag = stream.read_byte()
		stream.version_flag = self.version_flag
		self.version = stream.read_byte()
		stream.version = self.version
		self.bitswap = stream.read_byte()
		self.seventh_byte = stream.read_byte()
		self.user_version = stream.read_type(VersionInfo)
		stream.user_version = self.user_version

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.fres)
		stream.write_byte(self.version_flag)
		stream.version_flag = self.version_flag
		stream.write_byte(self.version)
		stream.version = self.version
		stream.write_byte(self.bitswap)
		stream.write_byte(self.seventh_byte)
		stream.write_type(self.user_version)
		stream.user_version = self.user_version

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'GenericHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* fres = {self.fres.__repr__()}'
		s += f'\n	* version_flag = {self.version_flag.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* bitswap = {self.bitswap.__repr__()}'
		s += f'\n	* seventh_byte = {self.seventh_byte.__repr__()}'
		s += f'\n	* user_version = {self.user_version.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
