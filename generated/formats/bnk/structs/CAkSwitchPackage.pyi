from generated.array import Array
from generated.base_struct import BaseStruct


class CAkSwitchPackage(BaseStruct):
    ul_switch_i_d: int
    ul_num_items: int
    nodes: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
