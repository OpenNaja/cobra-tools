from generated.base_enum import BaseEnum


class UbyteEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_ubyte()

	def write(self, stream):
		stream.write_ubyte(self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		cls.from_value(stream.read_ubyte())

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_ubyte(instance.value)


class Uint64Enum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_uint64()

	def write(self, stream):
		stream.write_uint64(self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		cls.from_value(stream.read_uint64())

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_uint64(instance.value)


class UintEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		cls.from_value(stream.read_uint())

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_uint(instance.value)


class UshortEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_ushort()

	def write(self, stream):
		stream.write_ushort(self.value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		cls.from_value(stream.read_ushort())

	@classmethod
	def to_stream(cls, stream, instance):
		stream.write_ushort(instance.value)
