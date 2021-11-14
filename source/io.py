from io import BytesIO
from struct import Struct

from contextlib import contextmanager
from typing import *

import numpy as np

from generated.array import Array

Byte = Struct("<b")  # int8
UByte = Struct("<B")  # uint8
Short = Struct("<h")  # int16
UShort = Struct("<H")  # uint16
Int = Struct("<i")  # int32
UInt = Struct("<I")  # uint32
Int64 = Struct("<q")  # int64
UInt64 = Struct("<Q")  # uint64
Float = Struct("<f")  # float32
HFloat = Struct("<e")  # float16

MAX_LEN = 1000


class BinaryStream(BytesIO):

	def __init__(self, initial_bytes=None):
		super().__init__(initial_bytes)

		(self.read_byte,
		 self.write_byte,
		 self.read_bytes,
		 self.write_bytes) = self.make_read_write_for_struct(Byte)

		(self.read_ubyte,
		 self.write_ubyte,
		 self.read_ubytes,
		 self.write_ubytes) = self.make_read_write_for_struct(UByte)

		(self.read_short,
		 self.write_short,
		 self.read_shorts,
		 self.write_shorts) = self.make_read_write_for_struct(Short)

		(self.read_ushort,
		 self.write_ushort,
		 self.read_ushorts,
		 self.write_ushorts) = self.make_read_write_for_struct(UShort)

		(self.read_int,
		 self.write_int,
		 self.read_ints,
		 self.write_ints) = self.make_read_write_for_struct(Int)

		(self.read_uint,
		 self.write_uint,
		 self.read_uints,
		 self.write_uints) = self.make_read_write_for_struct(UInt)

		(self.read_int64,
		 self.write_int64,
		 self.read_int64s,
		 self.write_int64s) = self.make_read_write_for_struct(Int64)

		(self.read_uint64,
		 self.write_uint64,
		 self.read_uint64s,
		 self.write_uint64s) = self.make_read_write_for_struct(UInt64)

		(self.read_float,
		 self.write_float,
		 self.read_floats,
		 self.write_floats) = self.make_read_write_for_struct(Float)

		(self.read_hfloat,
		 self.write_hfloat,
		 self.read_hfloats,
		 self.write_hfloats) = self.make_read_write_for_struct(HFloat)

		(self.read_string,
		 self.write_string,
		 self.read_strings,
		 self.write_strings) = self.make_read_write_for_string(UInt)

		(self.read_zstring,
		 self.write_zstring,
		 self.read_zstrings,
		 self.write_zstrings) = self.make_read_write_for_zstring()

	def make_read_write_for_struct(self, struct):
		# declare these in the local scope for faster name resolution
		read = self.read
		write = self.write
		pack = struct.pack
		unpack = struct.unpack
		size = struct.size
		# these functions are used for efficient read/write of arrays
		empty = np.empty
		dtype = np.dtype(struct.format)
		readinto = self.readinto

		def read_value():
			return unpack(read(size))[0]

		def write_value(value):
			write(pack(value))

		def read_values(shape):
			array = empty(shape, dtype)
			# noinspection PyTypeChecker
			readinto(array)
			return array

		def write_values(array):
			# check that it is a numpy array
			if not isinstance(array, np.ndarray):
				array = np.array(array, dtype)
			# cast if wrong incoming dtype
			elif array.dtype != dtype:
				array = array.astype(dtype)
			write(array.tobytes())

		return read_value, write_value, read_values, write_values

	def make_read_write_for_string(self, struct):
		# declare these in the local scope for faster name resolutions
		read = self.read
		write = self.write
		pack = struct.pack
		unpack = struct.unpack

		def read_string():
			value = read(*unpack(read(4)))
			return value.decode(errors="surrogateescape")

		def write_string(value):
			value = value.encode(errors="surrogateescape")
			write(pack(len(value)) + value)

		return read_string, write_string, NotImplemented, NotImplemented

	def read_type(self, cls, args=()):
		# obj = cls.__new__(cls, *args)
		obj = cls(*args)
		obj.read(self)
		return obj

	def write_type(self, obj):
		obj.write(self)

	def make_read_write_for_zstring(self,):
		# declare these in the local scope for faster name resolutions
		read = self.read
		write = self.write

		def read_zstring():
			i = 0
			val = b''
			char = b''
			while char != b'\x00':
				i += 1
				if i > MAX_LEN:
					raise ValueError('string too long')
				val += char
				char = read(1)
			return val.decode(errors="surrogateescape")

		def write_zstring(value):
			write(value.encode(errors="surrogateescape"))
			write(b'\x00')

		def read_zstrings(shape):
			# pass empty context
			arr = Array(None)
			arr.read(self, "zstring", shape)
			return arr

		def write_zstrings(arr):
			arr.write(self, "zstring")

		return read_zstring, write_zstring, read_zstrings, write_zstrings

	def get_io_func(self, dtype, mode="read"):
		func = f"{mode}_{dtype.lower()}"
		if func in self.__slots__:
			return getattr(self, func)
		else:
			raise NotImplementedError(f"No basic io function '{func}' for dtype {dtype}!")


class IoFile:

	def load(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)
			return stream.tell()

	def save(self, filepath):
		with self.writer(filepath) as stream:
			self.write(stream)
			return stream.tell()

	@staticmethod
	@contextmanager
	def reader(filepath) -> Generator[BinaryStream, None, None]:
		with open(filepath, "rb") as f:
			data = f.read()
		with BinaryStream(data) as stream:
			yield stream  # type: ignore

	@staticmethod
	@contextmanager
	def writer(filepath) -> Generator[BinaryStream, None, None]:
		with BinaryStream() as stream:
			yield stream  # type: ignore
			with open(filepath, "wb") as f:
				# noinspection PyTypeChecker
				f.write(stream.getbuffer())
