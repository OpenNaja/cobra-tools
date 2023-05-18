from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint64


class Key94(BasicBitfield):

	"""
	for 00 94 channel
	"""

	__name__ = 'Key94'
	_storage = Uint64
	loc_x = BitfieldMember(pos=0, mask=0x3fff, return_type=Int.from_value)
	loc_y = BitfieldMember(pos=14, mask=0xfffc000, return_type=Int.from_value)
	loc_z = BitfieldMember(pos=28, mask=0x3fff0000000, return_type=Int.from_value)
	rot_x = BitfieldMember(pos=42, mask=0x1fffc0000000000, return_type=Int.from_value)

	def set_defaults(self):
		pass
