from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.manis.basic import Int48
from generated.formats.ovl_base.basic import Bool


class PosBaseKey(BasicBitfield):

	__name__ = 'PosBaseKey'
	_storage = Int48
	loc_x = BitfieldMember(pos=0, mask=0x7fff, return_type=Int.from_value)
	loc_y = BitfieldMember(pos=15, mask=0x3fff8000, return_type=Int.from_value)
	loc_z = BitfieldMember(pos=30, mask=0x1fffc0000000, return_type=Int.from_value)
	key_x = BitfieldMember(pos=45, mask=0x200000000000, return_type=Bool.from_value)
	key_y = BitfieldMember(pos=46, mask=0x400000000000, return_type=Bool.from_value)
	key_z = BitfieldMember(pos=47, mask=0x800000000000, return_type=Bool.from_value)

	def set_defaults(self):
		pass
