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

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'magic', FixedString, (4, None), (False, None)
		yield 'version_flag', Byte, (0, None), (False, None)
		yield 'version', Byte, (0, None), (False, None)
		yield 'bitswap', Byte, (0, None), (False, None)
		yield 'seventh_byte', Byte, (0, None), (False, 1)
		yield 'user_version', VersionInfo, (0, None), (False, None)
