from struct import Struct


struct = Struct("<Q")


class String:

    def __new__(cls, context=None, arg=None, template=None):
        return ''

    @staticmethod
    def from_stream(stream, context=None, arg=None, template=None):
        value = stream.read(*struct.unpack(stream.read(4)))
        return value.decode(errors="surrogateescape")

    @staticmethod
    def to_stream(stream, instance):
        value = instance.encode(errors="surrogateescape")
        stream.write(struct.pack(len(value)) + value)

    @staticmethod
    def from_value(value, context=None, arg=None, template=None):
        return str(value)

    @classmethod
    def functions_for_stream(cls, ):
        raise NotImplementedError()