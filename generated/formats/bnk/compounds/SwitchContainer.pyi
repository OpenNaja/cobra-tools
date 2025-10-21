from generated.array import Array
from generated.formats.bnk.compounds.AkSwitchNodeParams import AkSwitchNodeParams
from generated.formats.bnk.compounds.CAkSwitchPackage import CAkSwitchPackage
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.compounds.NodeBaseParams import NodeBaseParams


class SwitchContainer(HircObject):
    node_base_params: NodeBaseParams
    e_group_type: int
    ul_group_i_d: int
    ul_default_switch: int
    b_is_continuous_validation: int
    num_children: int
    children: Array[int]
    ul_num_switch_groups: int
    switch_groups: Array[CAkSwitchPackage]
    ul_num_switch_params: int
    switch_node_params: Array[AkSwitchNodeParams]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
