from io import BytesIO
from struct import Struct
import zlib

from contextlib import contextmanager
from typing import *

import numpy as np

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


class BinaryStream(BytesIO):
    __slots__ = (
        "read_byte",
        "read_bytes",
        "read_ubyte",
        "read_ubytes",
        "read_short",
        "read_shorts",
        "read_ushort",
        "read_ushorts",
        "read_int",
        "read_ints",
        "read_uint",
        "read_uints",
        "read_int64",
        "read_int64s",
        "read_uint64",
        "read_uint64s",
        "read_float",
        "read_floats",
        "read_hfloat",
        "read_hfloats",
        "read_str",
        "read_strs",
        "write_byte",
        "write_bytes",
        "write_ubyte",
        "write_ubytes",
        "write_short",
        "write_shorts",
        "write_ushort",
        "write_ushorts",
        "write_int",
        "write_ints",
        "write_uint",
        "write_uints",
        "write_int64",
        "write_int64s",
        "write_uint64",
        "write_uint64s",
        "write_float",
        "write_floats",
        "write_hfloat",
        "write_hfloats",
        "write_str",
        "write_strs",
    )

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

        (self.read_str,
         self.write_str,
         self.read_strs,
         self.write_strs) = self.make_read_write_for_string(UInt)

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

        def read_values(*shape):
            array = empty(shape, dtype)
            # noinspection PyTypeChecker
            readinto(array)
            return array

        def write_values(array):
            if array.dtype != dtype:
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

    def read_array(self, shape, dtype=np.float32):  # TODO remove this
        array = np.empty(shape, dtype)
        # noinspection PyTypeChecker
        self.readinto(array)
        return array

    def write_array(self, array, dtype=np.float32):  # TODO remove this
        if array.dtype != dtype:
            array = array.astype(dtype)
        self.write(array.tobytes())

    def read_type(self, cls, args=()):
        # obj = cls.__new__(cls, *args)
        obj = cls(*args)
        obj.read(self)
        return obj

    def write_type(self, obj):
        obj.write(self)


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


class ZipFile(IoFile):

    # @staticmethod
    @contextmanager
    def unzipper(self, filepath, start, compressed_size, save_temp_dat=""):
        with self.reader(filepath) as stream:
            # self.unzip(stream, compressed_size)
            stream.seek(start)
            zipped = stream.read(compressed_size)
            # self.print_and_callback(f"Reading {archive_entry.name}")
            self.zlib_header = zipped[:2]
            zlib_compressed_data = zipped[2:]
            # https://stackoverflow.com/questions/1838699/how-can-i-decompress-a-gzip-stream-with-zlib
            # we avoid the two zlib magic bytes to get our unzipped content
            # zlib_data = bytearray(zlib.decompress(zlib_compressed_data, wbits=-zlib.MAX_WBITS))
            zlib_data = zlib.decompress(zlib_compressed_data, wbits=-zlib.MAX_WBITS)
        if save_temp_dat:
            # for debugging, write deflated content to dat
            with open(save_temp_dat, 'wb') as out:
                out.write(zlib_data)
        with BinaryStream(zlib_data) as stream:
            yield stream  # type: ignore
