from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class GateInfo(MemStruct):
    entrance_gate: Pointer[str]
    exit_gate: Pointer[str]
    unknown_ptr: Pointer[str]
    fence_extrusion: Pointer[str]
    small_fence_extrusion: Pointer[str]
    fence_cap: Pointer[str]
    floats: Array[float]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
