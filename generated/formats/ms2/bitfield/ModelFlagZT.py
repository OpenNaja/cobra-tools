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

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		return cls.from_value(stream.read_uint())

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_uint(instance._value)
