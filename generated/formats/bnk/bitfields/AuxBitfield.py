from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ubyte


class AuxBitfield(BasicBitfield):

	__name__ = 'AuxBitfield'
	_storage = Ubyte
	b_override_user_aux_sends = BitfieldMember(pos=2, mask=0x4, return_type=Int.from_value)
	b_has_aux = BitfieldMember(pos=3, mask=0x8, return_type=Int.from_value)
	b_override_reflections_aux_bus = BitfieldMember(pos=4, mask=0x10, return_type=Int.from_value)

	def set_defaults(self):
		pass
