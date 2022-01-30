from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class ModelFlag(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""
	stripify = BitfieldMember(pos=3, mask=0x8, return_type=bool)
	weights = BitfieldMember(pos=4, mask=0x10, return_type=bool)
	repeat_tris = BitfieldMember(pos=5, mask=0x20, return_type=bool)
	fur_shells = BitfieldMember(pos=8, mask=0x100, return_type=bool)
	basic_info = BitfieldMember(pos=9, mask=0x200, return_type=bool)

	def set_defaults(self):
		pass

	def read(self, stream):
		self._value = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value)
