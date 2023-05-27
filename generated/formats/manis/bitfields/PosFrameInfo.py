from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class PosFrameInfo(BasicBitfield):

	__name__ = 'PosFrameInfo'
	_storage = Uint
	ch_bit_size = BitfieldMember(pos=0, mask=0x1f, return_type=Int.from_value)

	def set_defaults(self):
		pass
