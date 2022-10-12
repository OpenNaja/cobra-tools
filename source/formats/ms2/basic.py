

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


class OffsetString(Int):

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		offset = super().from_stream(stream, context, arg, template)
		# arg must be ZStringBuffer
		return arg.get_str_at(offset)

	@classmethod
	def to_stream(cls, instance, stream, context, arg=0, template=None):
		# todo update ZStringBuffer before writing
		# arg = ZStringBuffer needs to be filled before writing
		# now we just take the index prepared by the string table
		offset = arg.offset_dic.get(instance, -1)
		# print(offset, instance, arg.offset_dic)
		super().to_stream(offset, stream, context, arg, template)
