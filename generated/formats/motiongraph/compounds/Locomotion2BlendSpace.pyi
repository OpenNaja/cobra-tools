from generated.formats.motiongraph.compounds.BlendSpaceAxis import BlendSpaceAxis
from generated.formats.motiongraph.compounds.Locomotion2BlendSpaceNode import Locomotion2BlendSpaceNode
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Locomotion2BlendSpace(MemStruct):
    y_axis: BlendSpaceAxis
    x_axis: BlendSpaceAxis
    nodes_count: int
    nodes: ArrayPointer[Locomotion2BlendSpaceNode]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
