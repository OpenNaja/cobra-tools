from struct import Struct

from generated.formats.base.basic import class_from_struct


Int64 = class_from_struct(Struct("<q"), lambda value: (int(value) + 9223372036854775808) % 18446744073709551616 - 9223372036854775808)


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
			'Int64': Int64,
}