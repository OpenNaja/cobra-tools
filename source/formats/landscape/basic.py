import logging
from struct import Struct

from generated.array import Array
from generated.formats.base.basic import Uint, Ushort, Ubyte, Int64


class NameOffset:

    def __new__(cls, context=None, arg=0, template=None):
        return ""

    @classmethod
    def from_stream(cls, stream, context, arg=0, template=None):
        offset = Uint.from_stream(stream, context, arg, template)
        try:
            return arg.get_str_at(offset)
        except (IndexError, ValueError):
            logging.warning(f"Index '{offset}' exceeds names list '{context.name_buffer.target_names}' at offset {stream.tell()}")
            return "bad_name"

    # @classmethod
    # def to_stream(cls, instance, stream, context, arg=0, template=None):
    #     # bones list needs to be filled before writing
    #     # now we just take the index prepared by the string table
    #     try:
    #         ind = context.name_buffer.target_names.index(instance)
    #     except (IndexError, ValueError):
    #         raise IndexError(f"String '{instance}' was missing from names list '{context.name_buffer.target_names}'")
    #     # print(offset, instance, arg.offset_dic)
    #     cls.cls_from_context(context).to_stream(ind, stream, context, arg, template)

    @staticmethod
    def format_indented(member, indent=0):
        return str(member)


class BoneIndex(Ubyte):

    @staticmethod
    def cls_from_arg(arg):
        if arg.use_ushort:
            return Ushort
        else:
            return Ubyte

    @classmethod
    def from_stream(cls, stream, context, arg=0, template=None):
        return cls.cls_from_arg(arg).from_stream(stream, context, arg, template)

    @classmethod
    def to_stream(cls, instance, stream, context, arg=0, template=None):
        cls.cls_from_arg(arg).to_stream(instance, stream, context, arg, template)

    @staticmethod
    def format_indented(member, indent=0):
        return str(member)


class Int48(Int64):
    mask = 0b111111111111111111111111111111111111111111111111

    def __new__(cls, context=None, arg=0, template=None):
        return 0

    @classmethod
    def from_stream(cls, stream, context, arg=0, template=None):
        c = stream.tell()
        ind = super().from_stream(stream, context, arg, template)
        stream.seek(c+6)
        return ind & cls.mask

    @classmethod
    def to_stream(cls, instance, stream, context, arg=0, template=None):
        ind = instance & cls.mask
        c = stream.tell()
        super().to_stream(ind, stream, context, arg, template)
        stream.seek(c+6)

    @staticmethod
    def format_indented(member, indent=0):
        return str(member)

