from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ushort


class ChannelSize(BasicBitfield):

	__name__ = 'ChannelSize'
	_storage = Ushort
	scl = BitfieldMember(pos=0, mask=0x1f, return_type=Int.from_value)
	loc = BitfieldMember(pos=5, mask=0x3e0, return_type=Int.from_value)
	rot = BitfieldMember(pos=10, mask=0x7c00, return_type=Int.from_value)
	unk = BitfieldMember(pos=15, mask=0x8000, return_type=Int.from_value)

	def set_defaults(self):
		pass
