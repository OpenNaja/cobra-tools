from generated.formats.helpnodedata.structs.HelpNode import HelpNode
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class HelpNodeDataHeader(MemStruct):
    parent_node: Pointer[str]
    parent_type: int
    node_count: int
    nodes: ArrayPointer[HelpNode]
    ptr_0: Pointer[object]
    ptr_1: Pointer[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
