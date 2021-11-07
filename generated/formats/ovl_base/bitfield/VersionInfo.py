from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class VersionInfo(BasicBitfield):

	"""
	Determines the format of the OVL file.
	n.b. pos counts from the end!
	"""
	unk_1 = BitfieldMember(pos=2, mask=0x4, return_type=bool)
	unk_2 = BitfieldMember(pos=4, mask=0x10, return_type=bool)
	use_zlib = BitfieldMember(pos=7, mask=0x80, return_type=bool)
	use_oodle = BitfieldMember(pos=9, mask=0x200, return_type=bool)
	unk_3 = BitfieldMember(pos=13, mask=0x2000, return_type=bool)
	is_jwe = BitfieldMember(pos=14, mask=0x4000, return_type=bool)

	def set_defaults(self):
		pass

	def read(self, stream):
		self._value = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value)
