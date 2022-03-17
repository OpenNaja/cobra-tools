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


class BasicBitfield(object):
    _value: int = 0

    def set_defaults(self):
        """This function has to be overwritten by concrete implementations to set defaults for the bitfield."""
        raise NotImplementedError

    def __hash__(self):
        return self._value.__hash__()

    def __int__(self):
        return self._value

    def __init__(self, context=None, arg=0, template=None, set_default=True):
        if set_default:
            self.set_defaults()
        else:
            self._value = 0

    @classmethod
    def from_value(cls, value):
        instance = cls(None, set_default=False)
        instance._value = value
        return instance

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        CALLABLES = types.FunctionType, types.MethodType
        fields = [key for key, value in self.__class__.__dict__.items() if not isinstance(value, CALLABLES) and not key.startswith("_")]
        info = f"<Bitfield> {self.__class__.__name__}: {self._value}, {bin(self._value)}"
        for field in fields:
            val = getattr(self, field)
            info += f"\n\t{field} = {str(val)}"
        return info

    # rich comparison methods
    def __lt__(self, other):
        return self._value < other

    def __le__(self, other):
        return self._value <= other

    def __eq__(self, other):
        return self._value == other

    def __ne__(self, other):
        return self._value != other

    def __gt__(self, other):
        return self._value > other

    def __ge__(self, other):
        return self._value >= other

    # basic arithmetic functions
    def __add__(self, other):
        return self._value + other

    def __sub__(self, other):
        return self._value - other

    def __mul__(self, other):
        return self._value * other

    def __truediv__(self, other):
        return self._value / other

    def __floordiv__(self, other):
        return self._value // other

    def __mod__(self, other):
        return self._value % other

    def __divmod__(self, other):
        return divmod(self._value, other)

    def __pow__(self, other, modulo=None):
        if modulo is None:
            return pow(self._value, other)
        else:
            return pow(self._value, other, modulo)

    def __lshift__(self, other):
        return self._value << other

    def __rshift__(self, other):
        return self._value >> other

    def __and__(self, other):
        return self._value & other

    def __xor__(self, other):
        return self._value ^ other

    def __or__(self, other):
        return self._value | other

    # reflected basic arithmetic functions
    def __radd__(self, other):
        return other + self._value

    def __rsub__(self, other):
        return other - self._value

    def __rmul__(self, other):
        return other * self._value

    def __rtruediv__(self, other):
        return other / self._value

    def __rfloordiv__(self, other):
        return other // self._value

    def __rmod__(self, other):
        return other % self._value

    def __rdivmod__(self, other):
        return divmod(other, self._value)

    def __rpow__(self, other, modulo=None):
        if modulo is None:
            return pow(other, self._value)
        else:
            return pow(other, self._value, modulo)

    def __rlshift__(self, other):
        return other << self._value

    def __rrshift__(self, other):
        return other >> self._value

    def __rand__(self, other):
        return other & self._value

    def __rxor__(self, other):
        return other ^ self._value

    def __ror__(self, other):
        return other | self._value

    # arithmetic assignments
    def __iadd__(self, other):
        self._value = int(self._value + other)
        return self

    def __isub__(self, other):
        self._value = int(self._value - other)
        return self

    def __imul__(self, other):
        self._value = int(self._value * other)
        return self

    def __itruediv__(self, other):
        self._value = int(self._value / other)
        return self

    def __ifloordiv__(self, other):
        self._value = int(self._value // other)
        return self

    def __imod__(self, other):
        self._value = int(self._value % other)
        return self

    def __ipow__(self, other, modulo=None):
        if modulo is None:
            self._value = int(pow(self._value, other))
        else:
            self._value = int(pow(self._value, other, modulo))
        return self

    def __ilshift__(self, other):
        self._value = int(self._value << other)
        return self

    def __irshift__(self, other):
        self._value = int(self._value >> other)
        return self

    def __iand__(self, other):
        self._value = int(self._value & other)
        return self

    def __ixor__(self, other):
        self._value = int(self._value ^ other)
        return self

    def __ior__(self, other):
        self._value = int(self._value | other)
        return self

    # unary operators
    def __neg__(self):
        return -self._value

    def __pos__(self):
        return +self._value

    def __abs__(self):
        return abs(self._value)

    def __invert__(self):
        return ~self._value

    def __complex__(self):
        return complex(self._value)

    def __float__(self):
        return float(self._value)

    def __index__(self):
        return self.__int__()


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


if __name__ == "__main__":
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


    temp2 = BasicBitfield.from_value(2)
    # temp3 = BasicBitfield()
    print(temp2)