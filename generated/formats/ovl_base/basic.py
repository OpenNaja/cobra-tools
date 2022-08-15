from struct import Struct

from generated.array import Array
from generated.formats.base.basic import class_from_struct, ZString, r_zstr, w_zstr

Bool = class_from_struct(Struct("<?"), bool)


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
            return Array.from_stream(stream, None, 0, None, shape, cls)

        def write_zstrings(instance):
            # pass empty context
            return Array.to_stream(stream, instance, instance.shape, cls, None)

        return read_zstring, write_zstring, read_zstrings, write_zstrings


from generated.formats.base.basic import Byte, Ubyte, Uint64, Int64, Uint, Ushort, Int, Short, Char, Float, Double, ZString