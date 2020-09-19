from enum import IntEnum
import types


class BitfieldMember(object):

    def __init__(self, pos=0, width=0, mask=0, return_type=bool):
        self.pos = pos
        self.mask = mask
        self.width = width
        self.return_type = return_type

    # see https://github.com/niftools/nifxml/issues/76 for reference
    def __get__(self, instance, owner):
        return self.return_type((instance._value & self.mask) >> self.pos)

    def __set__(self, instance, value):
        # Clear the current value
        instance._value = instance._value & ~self.mask
        # Update with the new value
        instance._value |= (value << self.pos) & self.mask


class BasicBitfield(int):
    _value: int = 0

    def set_defaults(self):
        """This function has to be overwritten by concrete implementations to set defaults for the bitfield."""
        raise NotImplementedError

    def __new__(cls, *args, **kwargs):
        return super(BasicBitfield, cls).__new__(cls)

    def __add__(self, other):
        self._value += other
        return self

    def __sub__(self, other):
        self._value -= other
        return self

    def __mul__(self, other):
        self._value *= other
        return self

    def __floordiv__(self, other):
        self._value //= other
        return self

    def __truediv__(self, other):
        self._value /= other
        return self

    def __init__(self, value=None):
        super().__init__()
        if value is not None:
            self._value = value
        else:
            self._value = 0
            self.set_defaults()

    def __repr__(self):
        return self.__str__

    def __str__(self):
        CALLABLES = types.FunctionType, types.MethodType
        fields = [key for key, value in self.__class__.__dict__.items() if not isinstance(value, CALLABLES) and not key.startswith("_")]
        info = f"<Bitfield> {self.__class__.__name__}: {self._value}, {bin(self._value)}"
        for field in fields:
            val = getattr(self, field)
            info += f"\n\t{field} = {str(val)}"
        return info


class AlphaFunction(IntEnum):
    """Describes alpha blend modes for NiAlphaProperty."""

    ONE = 0
    ZERO = 1
    SRC_COLOR = 2
    INV_SRC_COLOR = 3
    DEST_COLOR = 4
    INV_DEST_COLOR = 5
    SRC_ALPHA = 6
    INV_SRC_ALPHA = 7
    DEST_ALPHA = 8
    INV_DEST_ALPHA = 9
    SRC_ALPHA_SATURATE = 10


class AlphaFlags(BasicBitfield):
    alpha_blend = BitfieldMember(0, 1, 0x0001, int)
    src_blend = BitfieldMember(1, 4, 0x001E, AlphaFunction)

    def set_defaults(self):
        self.alpha_blend = 1
        self.src_blend = AlphaFunction.SRC_ALPHA

# AlphaFunction(1)
temp = AlphaFlags()
print(AlphaFunction.INV_DEST_ALPHA.value)
# # temp.value = 0
# print("alpha_blend", temp.alpha_blend, temp.value, bin(temp.value))
# temp.alpha_blend = 1
# print("alpha_blend", temp.alpha_blend, temp.value, bin(temp.value))
#
# print(temp)
print("src_blend", temp.src_blend, temp._value, bin(temp._value))
temp.src_blend = AlphaFunction.INV_DEST_ALPHA
print("src_blend", temp.src_blend, temp._value, bin(temp._value))
temp.src_blend &= 0
print("src_blend", temp.src_blend, temp._value, bin(temp._value))
# print("src_blend", temp.src_blend, temp.value, bin(temp.value))
temp += 3
print(temp)
temp = temp + 1
print(temp)
temp = temp +3
print(temp)
temp -= 2
print(temp)
temp *= 2
print(temp)
temp = temp // 4
print(temp)


temp2 = BasicBitfield(2)
# temp3 = BasicBitfield()
print(temp2)