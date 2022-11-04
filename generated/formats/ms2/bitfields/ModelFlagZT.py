from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Uint


class ModelFlagZT(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""

	__name__ = 'ModelFlagZT'
	_storage = Uint
	stripify = BitfieldMember(pos=6, mask=0x40, return_type=bool)
	repeat_tris = BitfieldMember(pos=9, mask=0x200, return_type=bool)

	def set_defaults(self):
		pass
