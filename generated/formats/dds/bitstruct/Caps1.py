from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class Caps1(BasicBitfield):
	reserved_1 = BitfieldMember(pos=0, mask=0x7, return_type=int)
	complex = BitfieldMember(pos=3, mask=0x8, return_type=int)
	reserved_2 = BitfieldMember(pos=4, mask=0xff0, return_type=int)
	texture = BitfieldMember(pos=12, mask=0x1000, return_type=int)
	reserved_3 = BitfieldMember(pos=13, mask=0x3fe000, return_type=int)
	mipmap = BitfieldMember(pos=22, mask=0x400000, return_type=int)

	def set_defaults(self):
		self.texture = 1

	def read(self, stream):
		self._value = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value)
