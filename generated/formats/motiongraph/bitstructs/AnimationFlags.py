from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember


class AnimationFlags(BasicBitfield):
	looping = BitfieldMember(pos=0, mask=0x1, return_type=int)
	additive = BitfieldMember(pos=1, mask=0x2, return_type=int)
	mirrored = BitfieldMember(pos=2, mask=0x4, return_type=int)
	affects_motion = BitfieldMember(pos=3, mask=0x8, return_type=int)
	flag_on_loop = BitfieldMember(pos=4, mask=0x10, return_type=int)
	reset_random_on_loop = BitfieldMember(pos=5, mask=0x20, return_type=int)
	suppress_resource_data_streams = BitfieldMember(pos=6, mask=0x40, return_type=int)

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
