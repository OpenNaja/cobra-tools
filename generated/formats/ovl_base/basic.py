from struct import Struct

from generated.formats.base.basic import class_from_struct


Bool = class_from_struct(Struct("<?"), bool)


from generated.formats.base.basic import Byte, Ubyte, Uint64, Uint, Ushort, Int, Short, Char, Float, ZString

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