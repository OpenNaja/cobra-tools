from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.basic import Bool


class ModelFlag(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""

	__name__ = 'ModelFlag'
	_storage = Uint
	unk_1 = BitfieldMember(pos=0, mask=0x7, return_type=Int.from_value)
	stripify = BitfieldMember(pos=3, mask=0x8, return_type=Bool.from_value)
	weights = BitfieldMember(pos=4, mask=0x10, return_type=Bool.from_value)
	repeat_tris = BitfieldMember(pos=5, mask=0x20, return_type=Bool.from_value)
	unk_2 = BitfieldMember(pos=6, mask=0xc0, return_type=Int.from_value)
	fur_shells = BitfieldMember(pos=8, mask=0x100, return_type=Bool.from_value)
	direct_address = BitfieldMember(pos=9, mask=0x200, return_type=Bool.from_value)

	def set_defaults(self):
		pass
