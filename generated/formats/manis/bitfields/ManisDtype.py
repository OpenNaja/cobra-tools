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
	ManisDtype: 0 0b0 ['unk = 0', 'compression = 0', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 1 0b1 ['unk = 1', 'compression = 0', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 4 0b100 ['unk = 0', 'compression = 1', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 5 0b101 ['unk = 1', 'compression = 1', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 6 0b110 ['unk = 2', 'compression = 1', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 8 0b1000 ['unk = 0', 'compression = 2', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 9 0b1001 ['unk = 1', 'compression = 2', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 14 0b1110 ['unk = 2', 'compression = 3', 'use_ushort = 0', 'has_list = 0']
	ManisDtype: 32 0b100000 ['unk = 0', 'compression = 0', 'use_ushort = 0', 'has_list = 1']
	ManisDtype: 34 0b100010 ['unk = 2', 'compression = 0', 'use_ushort = 0', 'has_list = 1']
	ManisDtype: 36 0b100100 ['unk = 0', 'compression = 1', 'use_ushort = 0', 'has_list = 1']
	ManisDtype: 37 0b100101 ['unk = 1', 'compression = 1', 'use_ushort = 0', 'has_list = 1']
	ManisDtype: 38 0b100110 ['unk = 2', 'compression = 1', 'use_ushort = 0', 'has_list = 1']
	ManisDtype: 64 0b1000000 ['unk = 0', 'compression = 0', 'use_ushort = 0', 'has_list = 2']
	ManisDtype: 66 0b1000010 ['unk = 2', 'compression = 0', 'use_ushort = 0', 'has_list = 2']
	ManisDtype: 68 0b1000100 ['unk = 0', 'compression = 1', 'use_ushort = 0', 'has_list = 2']
	ManisDtype: 69 0b1000101 ['unk = 1', 'compression = 1', 'use_ushort = 0', 'has_list = 2']
	ManisDtype: 70 0b1000110 ['unk = 2', 'compression = 1', 'use_ushort = 0', 'has_list = 2']
	ManisDtype: 82 0b1010010 ['unk = 2', 'compression = 0', 'use_ushort = 1', 'has_list = 2']
	"""

	__name__ = 'ManisDtype'
	_storage = Uint
	unk = BitfieldMember(pos=0, mask=0x3, return_type=Int.from_value)
	compression = BitfieldMember(pos=2, mask=0xc, return_type=Int.from_value)
	use_ushort = BitfieldMember(pos=4, mask=0x10, return_type=Int.from_value)
	has_list = BitfieldMember(pos=5, mask=0x60, return_type=Int.from_value)

	def set_defaults(self):
		pass
