from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class ManisDtypePC2(BasicBitfield):

	"""
	# PC2: 48, 112, 113, 114, more?
	"""

	__name__ = 'ManisDtypePC2'
	_storage = Uint
	unk = BitfieldMember(pos=0, mask=0x7, return_type=Int.from_value)
	use_ushort = BitfieldMember(pos=3, mask=0x8, return_type=Int.from_value)
	has_list = BitfieldMember(pos=4, mask=0x30, return_type=Int.from_value)
	compression = BitfieldMember(pos=6, mask=0x40, return_type=Int.from_value)

	def set_defaults(self):
		pass
