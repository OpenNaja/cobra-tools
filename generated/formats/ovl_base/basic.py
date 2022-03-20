from struct import Struct

from generated.array import Array
from generated.formats.base.basic import class_from_struct, ZString, r_zstr, w_zstr
from generated.io import BinaryStream

Bool = class_from_struct(Struct("<?"), bool)


class ConvStream(BinaryStream):
    """Just a convenience stream that has basic types available by default"""

    def __init__(self, initial_bytes=None):
        super().__init__(initial_bytes)
        self.register_basic_functions(basic_map)


separator = "::"


def r_zstr_obfuscated(r_func):
    _hash, _name = r_zstr(r_func).split(separator)
    name_str = _obfuscate(_name, delta=-1)
    return f"{_hash}{separator}{name_str}"


def w_zstr_obfuscated(w_func, s):
    _hash, _name = s.split(separator)
    name_str = _obfuscate(_name, delta=+1)
    w_zstr(w_func, f"{_hash}{separator}{name_str}")


def _obfuscate(s, delta=1):
    b = bytearray(s.encode())
    # decode the names
    for i in range(len(b)):
        b[i] = max(0, b[i] + delta)
    return b.decode()


class ZStringObfuscated(ZString):

    @staticmethod
    def from_stream(stream, context=None, arg=0, template=None):
        return r_zstr_obfuscated(stream.read)

    @staticmethod
    def to_stream(stream, instance):
        w_zstr_obfuscated(stream.write, instance)

    @classmethod
    def functions_for_stream(cls, stream):
        # declare these in the local scope for faster name resolutions
        read = stream.read
        write = stream.write

        def read_zstring():
            return r_zstr_obfuscated(read)

        def write_zstring(instance):
            w_zstr_obfuscated(write, instance)

        def read_zstrings(shape):
            # pass empty context
            return Array.from_stream(stream, shape, cls, None)

        def write_zstrings(instance):
            # pass empty context
            return Array.to_stream(stream, instance, instance.shape, cls, None)

        return read_zstring, write_zstring, read_zstrings, write_zstrings


from generated.formats.base.basic import Byte, Ubyte, Uint64, Uint, Ushort, Int, Short, Char, Float, ZString

basic_map = {
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
			'ZStringObfuscated': ZStringObfuscated,
}
