from enum import EnumMeta, IntEnum


# https://stackoverflow.com/questions/44867597/is-there-a-way-to-specify-a-default-value-for-python-enums
class DefaultEnumMeta(EnumMeta):
	default = object()

	def __call__(cls, value=default, *args, **kwargs):
		if value is DefaultEnumMeta.default:
			# Assume the first enum is default
			return next(iter(cls))
		return super().__call__(value, *args, **kwargs)

	# Execute base __new__ https://github.com/python/cpython/blob/32959108f9c543e3cb9f2b68bbc782bddded6f42/Lib/enum.py#L410
	# and then move __new__ to from_value, while the new __new__ accepts the standardized arguments
	def __new__(metacls, cls, bases, classdict):
		enum_class = super(metacls, metacls).__new__(metacls, cls, bases, classdict)
		new_function = enum_class.__new__
        # from_value doesn't need to be a proper __new__-like function, because specified enums can't be inherited from
		enum_class.from_value = classmethod(lambda cls, value: new_function(cls, value))
		enum_class.__new__ = lambda cls, context=None, arg=None, template=None, set_default=True: new_function(cls)
		return enum_class


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
