from struct import Struct


struct = Struct("<Q")
unpack = struct.unpack
pack = struct.pack

class String:

    def __new__(cls, context=None, arg=None, template=None):
        return ''

    @staticmethod
    def from_value(value, context=None, arg=None, template=None):
        return str(value)

    @staticmethod
    def from_stream(stream, context=None, arg=None, template=None):
        value = stream.read(*unpack(stream.read(4)))
        return value.decode(errors="surrogateescape")

    @staticmethod
    def to_stream(stream, instance):
        value = instance.encode(errors="surrogateescape")
        stream.write(pack(len(value)) + value)

    @staticmethod
    def functions_for_stream(stream):
        # declare these in the local scope for faster name resolutions
        read = stream.read
        write = stream.write

        def read_string():
            value = read(*unpack(read(4)))
            return value.decode(errors="surrogateescape")

        def write_string(value):
            value = value.encode(errors="surrogateescape")
            write(pack(len(value)) + value)

        return read_string, write_string, NotImplemented, NotImplemented

from generated.formats.ovl_base.basic import Byte, Ubyte, Uint64, Uint, Ushort, Int, Short, Char, Float, ZString, Bool

base_map = {
			'Byte': Byte,
			'Ubyte': Ubyte,
			'Uint64': Uint64,
			'Uint': Uint,
			'Ushort': Ushort,
			'Int': Int,
			'Short': Short,
			'Char': Char,
			'Float': Float,
			'ZString': ZString,
			'Bool': Bool,
}