from generated.formats.motiongraph.structs.BlendSpaceAxis import BlendSpaceAxis
from generated.formats.motiongraph.structs.Locomotion2BlendSpaceNode import Locomotion2BlendSpaceNode
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Locomotion2BlendSpace(MemStruct):
    y_axis: BlendSpaceAxis
    x_axis: BlendSpaceAxis
    nodes_count: int
    nodes: ArrayPointer[Locomotion2BlendSpaceNode]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
