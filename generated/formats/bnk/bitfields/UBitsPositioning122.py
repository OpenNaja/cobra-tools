from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ubyte


class UBitsPositioning122(BasicBitfield):

	__name__ = 'uBitsPositioning122'
	_storage = Ubyte
	b_positioning_info_override_parent = BitfieldMember(pos=0, mask=0x1, return_type=Int.from_value)
	unknown_2_d_next_flag = BitfieldMember(pos=1, mask=0x2, return_type=Int.from_value)
	unknown_2_d = BitfieldMember(pos=2, mask=0x4, return_type=Int.from_value)
	cb_is_3_d_positioning_available = BitfieldMember(pos=3, mask=0x8, return_type=Int.from_value)

	def set_defaults(self):
		pass
