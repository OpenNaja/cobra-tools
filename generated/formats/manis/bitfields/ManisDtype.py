from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class ManisDtype(BasicBitfield):

	"""
	# PZ dtypes: 0, 1, 4, 5, 6, 32, 34, 36, 37, 38
	# JWE2 dev dtypes: 0, 4, 5, 6, 32, 34, 36, 37, 38
	# JWE2 dtypes: 0, 4, 5, 6, 64, 66, 68, 69, 70
	ManisDtype: 0 0b0 ['compression = 0']
	ManisDtype: 1 0b1 ['compression = 1']
	ManisDtype: 4 0b100 ['compression = 4']
	ManisDtype: 5 0b101 ['compression = 5']
	ManisDtype: 6 0b110 ['compression = 6']
	ManisDtype: 32 0b100000 ['compression = 32']
	ManisDtype: 34 0b100010 ['compression = 34']
	ManisDtype: 36 0b100100 ['compression = 36']
	ManisDtype: 37 0b100101 ['compression = 37']
	ManisDtype: 38 0b100110 ['compression = 38']
	ManisDtype: 64 0b1000000 ['compression = 0', 'has_list = True']
	ManisDtype: 66 0b1000010 ['compression = 2', 'has_list = True']
	ManisDtype: 68 0b1000100 ['compression = 4', 'has_list = True']
	ManisDtype: 69 0b1000101 ['compression = 5', 'has_list = True']
	ManisDtype: 70 0b1000110 ['compression = 6', 'has_list = True']
	"""

	__name__ = 'ManisDtype'
	_storage = Uint
	compression = BitfieldMember(pos=0, mask=0x1f, return_type=Int.from_value)
	has_list = BitfieldMember(pos=5, mask=0x60, return_type=Int.from_value)

	def set_defaults(self):
		pass
