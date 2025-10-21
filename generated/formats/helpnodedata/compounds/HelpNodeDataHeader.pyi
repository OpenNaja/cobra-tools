from generated.formats.helpnodedata.compounds.HelpNode import HelpNode
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class HelpNodeDataHeader(MemStruct):
    parent_node: Pointer[str]
    parent_type: int
    node_count: int
    nodes: ArrayPointer[HelpNode]
    ptr_0: Pointer[object]
    ptr_1: Pointer[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
