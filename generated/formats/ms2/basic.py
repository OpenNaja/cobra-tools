

from generated.formats.base.basic import Uint, Int


class BiosynVersion(Uint):

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		value = super().from_stream(stream, context, arg, template)
		context.biosyn = value
		return value


class MainVersion(Uint):

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		value = super().from_stream(stream, context, arg, template)
		context.version = value
		return value



from generated.formats.ovl_base.basic import Byte, Ubyte, Uint64, Int64, Uint, Ushort, Int, Short, Char, Float, Double, ZString, Bool, OffsetString, ZStringObfuscated