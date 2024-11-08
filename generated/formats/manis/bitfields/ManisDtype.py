from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class ManisDtype(BasicBitfield):

	"""
	# ZTUAC: 14, probably more
	# PC: 0, 8, 9
	# PZ: 0, 1, 4, 5, 6, 32, 34, 36, 37, 38
	# JWE2 dev: 0, 4, 5, 6, 32, 34, 36, 37, 38
	# JWE2: 0, 4, 5, 6, 64, 66, 68, 69, 70
	# WH: unknown
	"""

	__name__ = 'ManisDtype'
	_storage = Uint
	unk = BitfieldMember(pos=0, mask=0x3, return_type=Int.from_value)
	compression = BitfieldMember(pos=2, mask=0xc, return_type=Int.from_value)
	use_ushort = BitfieldMember(pos=4, mask=0x10, return_type=Int.from_value)
	has_list = BitfieldMember(pos=5, mask=0x60, return_type=Int.from_value)

	def set_defaults(self):
		pass
