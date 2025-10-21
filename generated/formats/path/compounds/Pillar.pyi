from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Pillar(MemStruct):
    pillar_model: Pointer[str]
    cap_model: Pointer[str]
    fln_model: Pointer[str]
    unk_floats: Array[float]
    unk_int_2: int
    unk_int_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
