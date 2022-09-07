from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.ovl_base.bitfields.VersionInfo import VersionInfo
from generated.formats.ovl_base.compounds.FixedString import FixedString


class GenericHeader(BaseStruct):

	"""
	Found at the beginning of every OVL file
	"""

	__name__ = 'GenericHeader'

	_import_path = 'generated.formats.ovl_base.compounds.GenericHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

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
		super().set_defaults()
		self.magic = FixedString(self.context, 4, None)
		self.version_flag = 0
		self.version = 0
		self.bitswap = 0
		self.seventh_byte = 1
		self.user_version = VersionInfo(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.magic = FixedString.from_stream(stream, instance.context, 4, None)
		instance.version_flag = Byte.from_stream(stream, instance.context, 0, None)
		instance.context.version_flag = instance.version_flag
		instance.version = Byte.from_stream(stream, instance.context, 0, None)
		instance.context.version = instance.version
		instance.bitswap = Byte.from_stream(stream, instance.context, 0, None)
		instance.seventh_byte = Byte.from_stream(stream, instance.context, 0, None)
		instance.user_version = VersionInfo.from_stream(stream, instance.context, 0, None)
		instance.context.user_version = instance.user_version

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		FixedString.to_stream(stream, instance.magic)
		Byte.to_stream(stream, instance.version_flag)
		Byte.to_stream(stream, instance.version)
		Byte.to_stream(stream, instance.bitswap)
		Byte.to_stream(stream, instance.seventh_byte)
		VersionInfo.to_stream(stream, instance.user_version)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'magic', FixedString, (4, None), (False, None)
		yield 'version_flag', Byte, (0, None), (False, None)
		yield 'version', Byte, (0, None), (False, None)
		yield 'bitswap', Byte, (0, None), (False, None)
		yield 'seventh_byte', Byte, (0, None), (False, 1)
		yield 'user_version', VersionInfo, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'GenericHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
