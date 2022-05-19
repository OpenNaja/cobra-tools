from source.formats.base.basic import fmt_member
from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class ModelFlagDLA(BasicBitfield):

	"""
	Determines the data held by a mesh.
	"""
	vertex_offset = BitfieldMember(pos=1, mask=0x2, return_type=bool)
	stripify = BitfieldMember(pos=5, mask=0x20, return_type=bool)

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
