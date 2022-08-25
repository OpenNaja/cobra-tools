from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Uint


class BioModelFlag(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""

	__name__ = 'BioModelFlag'
	storage = Uint
	flat_arrays = BitfieldMember(pos=0, mask=0x1, return_type=bool)
	fur_shells = BitfieldMember(pos=2, mask=0x4, return_type=bool)
	fur_shells_2 = BitfieldMember(pos=3, mask=0x8, return_type=bool)

	def set_defaults(self):
		pass
