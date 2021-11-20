from generated.context import ContextReference
from generated.formats.ovl_base.bitfield.VersionInfo import VersionInfo
from generated.formats.ovl_base.compound.FixedString import FixedString


class GenericHeader:

	"""
	Found at the beginning of every OVL file
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FGM ' for fgm, 'FRES' for ovl, 'MANI' for manis, 'MS2 ' for ms2, 'VOXE' for voxelskirt
		self.magic = FixedString(self.context, 4, None)

		# if 0x08 then 64bit, 0x01 for JWE, PZ, 0x08 for PC, 0x48 for JWE Switch, may be platform
		self.version_flag = 0

		# 0x12 = PC, 0x13 = JWE, PZ
		self.version = 0

		# endianness?, usually zero
		self.bitswap = 0

		# always = 1
		self.seventh_byte = 1

		# determines compression format (none, zlib or oodle) and apparently type of data (additional fields)
		self.user_version = VersionInfo(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.magic = FixedString(self.context, 4, None)
		self.version_flag = 0
		self.version = 0
		self.bitswap = 0
		self.seventh_byte = 1
		self.user_version = VersionInfo(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.magic = stream.read_type(FixedString, (self.context, 4, None))
		self.version_flag = stream.read_byte()
		self.context.version_flag = self.version_flag
		self.version = stream.read_byte()
		self.context.version = self.version
		self.bitswap = stream.read_byte()
		self.seventh_byte = stream.read_byte()
		self.user_version = stream.read_type(VersionInfo)
		self.context.user_version = self.user_version

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.magic)
		stream.write_byte(self.version_flag)
		stream.write_byte(self.version)
		stream.write_byte(self.bitswap)
		stream.write_byte(self.seventh_byte)
		stream.write_type(self.user_version)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'GenericHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* magic = {self.magic.__repr__()}'
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
