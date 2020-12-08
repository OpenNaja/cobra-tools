from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class ModelFlag(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""
	basic_info = BitfieldMember(pos=0, mask=0x1, return_type=bool)

	def set_defaults(self):
		pass

	def read(self, stream):
		self._value = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value)
