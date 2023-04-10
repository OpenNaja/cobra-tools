from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Ushort


class RenderFlag(BasicBitfield):

	"""
	Determines how the model is rendered.
	"""

	__name__ = 'RenderFlag'
	_storage = Ushort
	a = BitfieldMember(pos=0, mask=0x1, return_type=Bool.from_value)
	b = BitfieldMember(pos=1, mask=0x2, return_type=Bool.from_value)
	c = BitfieldMember(pos=2, mask=0x4, return_type=Bool.from_value)
	d = BitfieldMember(pos=3, mask=0x8, return_type=Bool.from_value)
	e = BitfieldMember(pos=4, mask=0x10, return_type=Bool.from_value)

	def set_defaults(self):
		pass
