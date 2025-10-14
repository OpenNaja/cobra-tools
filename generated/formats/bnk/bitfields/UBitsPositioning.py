from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ubyte


class UBitsPositioning(BasicBitfield):

	__name__ = 'uBitsPositioning'
	_storage = Ubyte
	b_positioning_info_override_parent = BitfieldMember(pos=0, mask=0x1, return_type=Int.from_value)
	b_has_listener_relative_routing = BitfieldMember(pos=1, mask=0x2, return_type=Int.from_value)
	e_panner_type = BitfieldMember(pos=2, mask=0xc, return_type=Int.from_value)
	e_3_d_position_type = BitfieldMember(pos=5, mask=0x60, return_type=Int.from_value)

	def set_defaults(self):
		pass
