from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Int64


class Key94C(BasicBitfield):

	"""
	for 00 94 channel
	"""

	__name__ = 'Key94C'
	_storage = Int64
	type = BitfieldMember(pos=0, mask=0x3, return_type=Int.from_value)
	loc_x = BitfieldMember(pos=2, mask=0x3fffffc, return_type=Int.from_value)
	loc_y = BitfieldMember(pos=26, mask=0xfffc000000, return_type=Int.from_value)
	loc_z = BitfieldMember(pos=40, mask=0x1f0000000000, return_type=Int.from_value)
	rot_rel = BitfieldMember(pos=45, mask=0xe00000000000, return_type=Int.from_value)
	rot_x_val = BitfieldMember(pos=48, mask=0xffff000000000000, return_type=Int.from_value)
	rot_y_val = BitfieldMember(pos=64, mask=0xffff0000000000000000, return_type=Int.from_value)
	rot_z_val = BitfieldMember(pos=80, mask=0xffff00000000000000000000, return_type=Int.from_value)

	def set_defaults(self):
		pass
