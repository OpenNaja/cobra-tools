from generated.formats.motiongraph.compounds.SubNestedZStr import SubNestedZStr
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class NestedZStr(MemStruct):
    bc: Pointer[SubNestedZStr]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
