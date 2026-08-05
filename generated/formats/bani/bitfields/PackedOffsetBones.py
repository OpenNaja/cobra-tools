from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint


class PackedOffsetBones(BasicBitfield):

	__name__ = 'PackedOffsetBones'
	_storage = Uint
	bone_channels_offset = BitfieldMember(pos=0, mask=0xffffff, return_type=Uint.from_value)
	num_bones = BitfieldMember(pos=24, mask=0xff000000, return_type=Ubyte.from_value)

	def set_defaults(self):
		pass
