from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ushort


class SegmentInfo(BasicBitfield):

	__name__ = 'SegmentInfo'
	_storage = Ushort
	not_last = BitfieldMember(pos=9, mask=0x200, return_type=Int.from_value)
	unk = BitfieldMember(pos=10, mask=0xffc00, return_type=Int.from_value)

	def set_defaults(self):
		pass
