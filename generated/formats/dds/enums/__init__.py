from generated.base_enum import BaseEnum

from generated.formats.dds.basic import Ubyte


class UbyteEnum(BaseEnum):

	def read(self, stream):
		self._value_ = Ubyte.from_stream(stream, None, 0, None)

	def write(self, stream):
		Ubyte.to_stream(stream, self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		instance = cls.from_value(Ubyte.from_stream(stream, None, 0, None))
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		Ubyte.to_stream(stream, instance.value)
		return instance

from generated.formats.dds.basic import Ushort


class UshortEnum(BaseEnum):

	def read(self, stream):
		self._value_ = Ushort.from_stream(stream, None, 0, None)

	def write(self, stream):
		Ushort.to_stream(stream, self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		instance = cls.from_value(Ushort.from_stream(stream, None, 0, None))
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		Ushort.to_stream(stream, instance.value)
		return instance

from generated.formats.dds.basic import Uint


class UintEnum(BaseEnum):

	def read(self, stream):
		self._value_ = Uint.from_stream(stream, None, 0, None)

	def write(self, stream):
		Uint.to_stream(stream, self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		instance = cls.from_value(Uint.from_stream(stream, None, 0, None))
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		Uint.to_stream(stream, instance.value)
		return instance
