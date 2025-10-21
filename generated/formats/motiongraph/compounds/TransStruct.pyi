from generated.formats.motiongraph.compounds.StateArray import StateArray
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TransStruct(MemStruct):
    another_mrf_reference_2: Pointer[object]
    states: StateArray

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
