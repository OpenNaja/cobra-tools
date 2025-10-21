from generated.formats.motiongraph.structs.State import State
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class StateReference(MemStruct):
    state: Pointer[State]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
