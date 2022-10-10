

from generated.formats.base.basic import Uint


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


class OffsetString(Uint):

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		offset = super().from_stream(stream, context, arg, template)
		# arg must be ZStringBuffer
		return arg.get_str_at(offset)

	@staticmethod
	def to_stream(stream, instance):
		raise NotImplementedError("OffsetString needs implementation for writing")
