from generated.array import Array
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.path.structs.SubBrace import SubBrace
from generated.formats.path.structs.SupportSetData import SupportSetData


class LatticeSupportSetRoot(MemStruct):
    model_00: Pointer[str]
    model_08: Pointer[str]
    model_16: Pointer[str]
    model_24: Pointer[str]
    unk_floats: Array[float]
    sub_braces: ArrayPointer[SubBrace]
    num_sub_brace: int
    data: ArrayPointer[SupportSetData]
    num_data: int
    padding: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
