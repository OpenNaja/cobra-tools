from generated.formats.base.basic import fmt_member
from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class RenderFlag(BasicBitfield):

	"""
	Determines how the model is rendered.
	"""
	a = BitfieldMember(pos=0, mask=0x1, return_type=bool)
	b = BitfieldMember(pos=1, mask=0x2, return_type=bool)
	c = BitfieldMember(pos=2, mask=0x4, return_type=bool)
	d = BitfieldMember(pos=3, mask=0x8, return_type=bool)
	e = BitfieldMember(pos=4, mask=0x10, return_type=bool)

	def set_defaults(self):
		pass

	def read(self, stream):
		self._value = stream.read_ushort()

	def write(self, stream):
		stream.write_ushort(self._value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		return cls.from_value(stream.read_ushort())

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_ushort(instance._value)
