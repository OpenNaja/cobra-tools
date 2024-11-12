from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class ManisDtypePC2(BasicBitfield):

	"""
	# PC2: 0, 48, 49, 112, 113, 114 (2024-11-12)
	"""

	__name__ = 'ManisDtypePC2'
	_storage = Uint
	unk = BitfieldMember(pos=0, mask=0x7, return_type=Int.from_value)
	use_ushort = BitfieldMember(pos=3, mask=0x8, return_type=Int.from_value)
	compression = BitfieldMember(pos=4, mask=0x10, return_type=Int.from_value)
	has_list = BitfieldMember(pos=5, mask=0x60, return_type=Int.from_value)

	def set_defaults(self):
		pass
