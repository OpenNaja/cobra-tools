from generated.array import Array
from generated.formats.bnk.structs.CAkLayer import CAkLayer
from generated.formats.bnk.structs.HircObject import HircObject
from generated.formats.bnk.structs.NodeBaseParams import NodeBaseParams


class BlendContainer(HircObject):
    node_base_params: NodeBaseParams
    num_children: int
    children: Array[int]
    ul_num_layers: int
    layers: Array[CAkLayer]
    b_is_continuous_validation: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
