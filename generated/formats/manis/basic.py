import logging
from struct import Struct

from generated.array import Array
from generated.formats.base.basic import class_from_struct, ZString, r_zstr, w_zstr, Uint, Ushort


class Channelname:

    # ushort_struct = Struct("<H")
    # uint_struct = Struct("<I")
    #
    # # _byte_from_value = lambda value: (int(value) + 128) % 256 - 128
    # # _int_from_value = lambda value: (int(value) + 2147483648) % 4294967296 - 2147483648
    #
    # @classmethod
    # def update_struct(cls, context):
    #     if context.version <= 257:
    #         # until PC - use ushort
    #         # cls.from_value = staticmethod(cls._int_from_value)
    #         cls.set_struct(cls.ushort_struct)
    #     else:
    #         # since JWE1 - use uint
    #         # cls.from_value = staticmethod(cls._byte_from_value)
    #         cls.set_struct(cls.uint_struct)
    #
    #     @classmethod
    #     def validate_array(cls, instance, context=None, arg=0, template=None, shape=()):
    #         assert instance.shape == shape
    #         assert instance.dtype.char in ("b", "i")

    @staticmethod
    def cls_from_context(context):
        if context.version <= 257:
            return Ushort
        else:
            return Uint

    @classmethod
    def from_stream(cls, stream, context, arg=0, template=None):
        ind = cls.cls_from_context(context).from_stream(stream, context, arg, template)
        return context.name_buffer.bone_names[ind]

    @classmethod
    def to_stream(cls, instance, stream, context, arg=0, template=None):
        # bones list needs to be filled before writing
        # now we just take the index prepared by the string table
        try:
            ind = context.name_buffer.bone_names.index[instance]
        except IndexError:
            raise IndexError(f"String '{instance}' was missing from names list '{context.name_buffer.bone_names}'")
        # print(offset, instance, arg.offset_dic)
        cls.cls_from_context(context).to_stream(ind, stream, context, arg, template)

    @staticmethod
    def fmt_member(member, indent=0):
        return str(member)
