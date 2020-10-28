from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class ModelFlag(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""
	active = BitfieldMember(pos=3, mask=0x8, return_type=bool)
	basic_info = BitfieldMember(pos=4, mask=0x10, return_type=bool)
	manager_controlled = BitfieldMember(pos=5, mask=0x20, return_type=bool)
	compute_scaled_time = BitfieldMember(pos=6, mask=0x40, return_type=bool)
	weights = BitfieldMember(pos=7, mask=0x80, return_type=bool)

	def set_defaults(self):
		self.active = 1
		self.compute_scaled_time = 1

	def read(self, stream):
		self._value = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value)
