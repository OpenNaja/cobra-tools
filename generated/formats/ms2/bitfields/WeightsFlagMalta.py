from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Ushort
from generated.formats.ms2.enums.MeshFormat import MeshFormat


class WeightsFlagMalta(BasicBitfield):

	__name__ = 'WeightsFlagMalta'
	_storage = Ushort
	mesh_format = BitfieldMember(pos=0, mask=0x3, return_type=MeshFormat.from_value)
	has_weights = BitfieldMember(pos=3, mask=0x8, return_type=bool)
	bone_index = BitfieldMember(pos=4, mask=0xff0, return_type=int)

	def set_defaults(self):
		pass
