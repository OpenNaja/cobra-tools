from generated.formats.voxelskirt.bitfield.VersionInfo import VersionInfo
from generated.formats.voxelskirt.compound.FixedString import FixedString
from generated.formats.voxelskirt.compound.SizedStrData import SizedStrData


class Header:

	"""
	Found at the beginning of every OVL file
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'VOXE'
		self.magic = FixedString()

		# if 0x08 then 64bit, differentiates between ED and JWE, 0x08 for ED and PC
		self.version_flag = 0

		# 0x12 = PC, 0x13 = JWE, PZ
		self.version = 0

		# endianness?, usually zero
		self.bitswap = 0

		# always = 1
		self.seventh_byte = 1

		# determines compression format (none, zlib or oodle) and apparently type of data (additional fields)
		self.user_version = VersionInfo()

		# always = 0
		self.info = SizedStrData()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic = stream.read_type(FixedString, (4,))
		self.version_flag = stream.read_byte()
		stream.version_flag = self.version_flag
		self.version = stream.read_byte()
		stream.version = self.version
		self.bitswap = stream.read_byte()
		self.seventh_byte = stream.read_byte()
		self.user_version = stream.read_type(VersionInfo)
		stream.user_version = self.user_version
		self.info = stream.read_type(SizedStrData)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.magic)
		stream.write_byte(self.version_flag)
		stream.version_flag = self.version_flag
		stream.write_byte(self.version)
		stream.version = self.version
		stream.write_byte(self.bitswap)
		stream.write_byte(self.seventh_byte)
		stream.write_type(self.user_version)
		stream.user_version = self.user_version
		stream.write_type(self.info)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Header [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+'] ' + self.name
		s += '\n	* magic = ' + self.magic.__repr__()
		s += '\n	* version_flag = ' + self.version_flag.__repr__()
		s += '\n	* version = ' + self.version.__repr__()
		s += '\n	* bitswap = ' + self.bitswap.__repr__()
		s += '\n	* seventh_byte = ' + self.seventh_byte.__repr__()
		s += '\n	* user_version = ' + self.user_version.__repr__()
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n'
		return s
