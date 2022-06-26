from source.formats.base.basic import fmt_member
from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class BioModelFlag(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""
	flat_arrays = BitfieldMember(pos=0, mask=0x1, return_type=bool)
	fur_shells = BitfieldMember(pos=2, mask=0x4, return_type=bool)
	fur_shells_2 = BitfieldMember(pos=3, mask=0x8, return_type=bool)

	def set_defaults(self):
		pass

	def read(self, stream):
		self._value = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		return cls.from_value(stream.read_uint())

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_uint(instance._value)
