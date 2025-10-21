from generated.array import Array
from generated.formats.guestonrideanimsettings.compounds.AnimPair import AnimPair
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RideAnims(MemStruct):
    anim_name: Pointer[str]
    am: Pointer[str]
    af: Pointer[str]
    tm: Pointer[str]
    tf: Pointer[str]
    cf: Pointer[str]
    cm: Pointer[str]
    bools: Array[int]
    floats: Array[float]
    anims: ArrayPointer[AnimPair]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
