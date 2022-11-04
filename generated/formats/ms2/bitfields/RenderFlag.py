from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Ushort


class RenderFlag(BasicBitfield):

	"""
	Determines how the model is rendered.
	"""

	__name__ = 'RenderFlag'
	_storage = Ushort
	a = BitfieldMember(pos=0, mask=0x1, return_type=bool)
	b = BitfieldMember(pos=1, mask=0x2, return_type=bool)
	c = BitfieldMember(pos=2, mask=0x4, return_type=bool)
	d = BitfieldMember(pos=3, mask=0x8, return_type=bool)
	e = BitfieldMember(pos=4, mask=0x10, return_type=bool)

	def set_defaults(self):
		pass
