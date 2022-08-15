from struct import Struct

from generated.array import Array


class String:

    _count_struct = Struct("<Q")
    _count_pack = _count_struct.pack
    _count_unpack = _count_struct.unpack

    def __new__(cls, context=None, arg=0, template=None):
        return ''

    @staticmethod
    def from_stream(stream, context=None, arg=0, template=None):
        value = stream.read(*_count_unpack(stream.read(4)))
        return value.decode(errors="surrogateescape")

    @staticmethod
    def to_stream(stream, instance):
        value = instance.encode(errors="surrogateescape")
        stream.write(_count_pack(len(value)) + value)

    @staticmethod
    def from_value(value, context=None, arg=0, template=None):
        return str(value)

    @classmethod
    def functions_for_stream(cls, stream):
        # declare these in the local scope for faster name resolutions
        read = stream.read
        write = stream.write

        def read_string():
            value = read(*_count_unpack(read(4)))
            return value.decode(errors="surrogateescape")
        
        def write_string(instance):
            value = instance.encode(errors="surrogateescape")
            write(_count_pack(len(value)) + value)
        
        def read_strings(shape):
            # pass empty context
            return Array.from_stream(stream, None, 0, None, shape, cls)
            
        def write_strings(instance):
            # pass empty context
            return Array.to_stream(stream, instance, cls, None)

        return read_string, write_string, read_strings, write_strings

    @staticmethod
    def from_xml(target, elem, prop, arguments=None):
        return elem[prop]

    @classmethod
    def to_xml(elem, prop, instance, arguments, debug):
        elem.attrib[prop] = instance
