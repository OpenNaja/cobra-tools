from generated.formats.motiongraph.compounds.State import State
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class StateReference(MemStruct):
    state: Pointer[State]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
