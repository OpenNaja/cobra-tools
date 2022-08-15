from struct import Struct

from generated.formats.base.basic import class_from_struct


Int64 = class_from_struct(Struct("<q"), lambda value: (int(value) + 9223372036854775808) % 18446744073709551616 - 9223372036854775808)


from generated.formats.ovl_base.basic import Byte, Ubyte, Uint64, Int64, Uint, Ushort, Int, Short, Char, Float, Double, ZString, Bool, ZStringObfuscated