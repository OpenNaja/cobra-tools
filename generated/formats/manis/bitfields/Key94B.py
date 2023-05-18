from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint64


class Key94B(BasicBitfield):

	"""
	for 00 94 channel
	"""

	__name__ = 'Key94b'
	_storage = Uint64
	loc_x = BitfieldMember(pos=0, mask=0x1fff, return_type=Int.from_value)
	loc_y = BitfieldMember(pos=13, mask=0x3ffe000, return_type=Int.from_value)
	loc_z = BitfieldMember(pos=26, mask=0x7ffc000000, return_type=Int.from_value)
	more_loc = BitfieldMember(pos=39, mask=0x3f8000000000, return_type=Int.from_value)
	rot_rel = BitfieldMember(pos=46, mask=0xc00000000000, return_type=Int.from_value)

	def set_defaults(self):
		pass
