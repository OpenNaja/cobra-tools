from generated.formats.motiongraph.structs.SubNestedZStr import SubNestedZStr
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class NestedZStr(MemStruct):
    bc: Pointer[SubNestedZStr]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
