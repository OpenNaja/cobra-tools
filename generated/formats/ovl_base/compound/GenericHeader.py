from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Byte
from generated.formats.ovl_base.bitfield.VersionInfo import VersionInfo
from generated.formats.ovl_base.compound.FixedString import FixedString
from generated.struct import StructBase


class GenericHeader(StructBase):

	"""
	Found at the beginning of every OVL file
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 'FGM ' for fgm, 'FRES' for ovl, 'MANI' for manis, 'MS2 ' for ms2, 'VOXE' for voxelskirt
		self.magic = 0

		# if 0x08 then 64bit, 0x01 for JWE, PZ, 0x08 for PC, 0x48 for JWE Switch, may be platform
		self.version_flag = 0

		# 0x12 = PC, 0x13 = JWE, PZ
		self.version = 0

		# endianness?, usually zero
		self.bitswap = 0

		# always = 1
		self.seventh_byte = 0

		# determines compression format (none, zlib or oodle) and apparently type of data (additional fields)
		self.user_version = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.magic = FixedString(self.context, 4, None)
		self.version_flag = 0
		self.version = 0
		self.bitswap = 0
		self.seventh_byte = 1
		self.user_version = VersionInfo(self.context, 0, None)

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
		instance.magic = FixedString.from_stream(stream, instance.context, 4, None)
		instance.version_flag = stream.read_byte()
		instance.context.version_flag = instance.version_flag
		instance.version = stream.read_byte()
		instance.context.version = instance.version
		instance.bitswap = stream.read_byte()
		instance.seventh_byte = stream.read_byte()
		instance.user_version = VersionInfo.from_stream(stream, instance.context, 0, None)
		instance.context.user_version = instance.user_version

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		FixedString.to_stream(stream, instance.magic)
		stream.write_byte(instance.version_flag)
		stream.write_byte(instance.version)
		stream.write_byte(instance.bitswap)
		stream.write_byte(instance.seventh_byte)
		VersionInfo.to_stream(stream, instance.user_version)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('magic', FixedString, (4, None))
		yield ('version_flag', Byte, (0, None))
		yield ('version', Byte, (0, None))
		yield ('bitswap', Byte, (0, None))
		yield ('seventh_byte', Byte, (0, None))
		yield ('user_version', VersionInfo, (0, None))

	def get_info_str(self, indent=0):
		return f'GenericHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* magic = {fmt_member(self.magic, indent+1)}'
		s += f'\n	* version_flag = {fmt_member(self.version_flag, indent+1)}'
		s += f'\n	* version = {fmt_member(self.version, indent+1)}'
		s += f'\n	* bitswap = {fmt_member(self.bitswap, indent+1)}'
		s += f'\n	* seventh_byte = {fmt_member(self.seventh_byte, indent+1)}'
		s += f'\n	* user_version = {fmt_member(self.user_version, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
