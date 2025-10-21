from generated.formats.motiongraph.structs.StateArray import StateArray
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class TransStruct(MemStruct):
    another_mrf_reference_2: Pointer[object]
    states: StateArray

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
