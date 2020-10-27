from enum import EnumMeta, IntEnum


# https://stackoverflow.com/questions/44867597/is-there-a-way-to-specify-a-default-value-for-python-enums
class DefaultEnumMeta(EnumMeta):
	default = object()

	def __call__(cls, value=default, *args, **kwargs):
		if value is DefaultEnumMeta.default:
			# Assume the first enum is default
			return next(iter(cls))
		return super().__call__(value, *args, **kwargs)
		# return super(DefaultEnumMeta, cls).__call__(value, *args, **kwargs) # PY2
	#
	# def __new__(cls, value=0):
	# 	member = object.__new__(cls)
	# 	member._value_ = value
	# 	return member


class BaseEnum(IntEnum, metaclass=DefaultEnumMeta):

	def __int__(self):
		return self.value
	pass


class UbyteEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_ubyte()

	def write(self, stream):
		stream.write_ubyte(self._value_)


class UshortEnum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_ushort()

	def write(self, stream):
		stream.write_ushort(self._value_)


class UintEnum(BaseEnum):

	def read(self, stream):
		u = stream.read_uint()
		# print(self.__class__(u))
		self = self.__class__(u)

	def write(self, stream):
		stream.write_uint(self._value_)


class Uint64Enum(BaseEnum):

	def read(self, stream):
		self._value_ = stream.read_uint64()

	def write(self, stream):
		stream.write_uint64(self._value_)
