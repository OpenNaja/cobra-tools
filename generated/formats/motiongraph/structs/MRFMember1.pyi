from generated.formats.motiongraph.structs.MRFChild import MRFChild
from generated.formats.motiongraph.structs.MotiongraphVars import MotiongraphVars
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MRFMember1(MemStruct):
    lua_method: Pointer[str]
    count_0: int
    ptr_0: Pointer[object]
    motiongraph_vars: Pointer[MotiongraphVars]
    dtype: int
    num_children: int
    children: ArrayPointer[MRFChild]
    count_4: int
    id: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
