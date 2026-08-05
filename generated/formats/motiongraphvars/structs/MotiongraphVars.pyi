from generated.array import Array
from generated.formats.motiongraphvars.structs.MotiongraphVarNew import MotiongraphVarNew
from generated.formats.ovl_base.structs.NestedPointers import NestedPointers
from generated.formats.ovl_base.structs.Pointer import Pointer


class MotiongraphVars(NestedPointers):
    ptrs: Array[Pointer[MotiongraphVarNew]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
