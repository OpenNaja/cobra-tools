from struct import Struct

from generated.formats.base.basic import class_from_struct
from generated.io import BinaryStream

Bool = class_from_struct(Struct("<?"), bool)


class ConvStream(BinaryStream):
	"""Just a convenience stream that has basic types available by default"""

	def __init__(self, initial_bytes=None):
		super().__init__(initial_bytes)
		self.register_basic_functions(basic_map)


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
}
