from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ushort
from generated.formats.ms2.enums.MeshFormat import MeshFormat
from generated.formats.ovl_base.basic import Bool


class WeightsFlag(BasicBitfield):

	__name__ = 'WeightsFlag'
	_storage = Ushort
	has_weights = BitfieldMember(pos=0, mask=0x1, return_type=Bool.from_value)
	bone_index = BitfieldMember(pos=1, mask=0x1fe, return_type=Int.from_value)
	mesh_format = BitfieldMember(pos=9, mask=0xfe00, return_type=MeshFormat.from_value)

	def set_defaults(self):
		pass
