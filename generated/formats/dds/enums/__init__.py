from generated.base_enum import BaseEnum


class UbyteEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_ubyte()

	def write(self, stream):
		stream.write_ubyte(self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		instance = cls.from_value(stream.read_ubyte())
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_ubyte(instance.value)
		return instance


class UshortEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_ushort()

	def write(self, stream):
		stream.write_ushort(self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		instance = cls.from_value(stream.read_ushort())
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_ushort(instance.value)
		return instance


class UintEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		instance = cls.from_value(stream.read_uint())
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_uint(instance.value)
		return instance
