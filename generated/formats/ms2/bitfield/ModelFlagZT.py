from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class ModelFlagZT(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""
	stripify = BitfieldMember(pos=6, mask=0x40, return_type=bool)
	repeat_tris = BitfieldMember(pos=9, mask=0x200, return_type=bool)

	def set_defaults(self):
		pass

	def read(self, stream):
		self._value = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value)
