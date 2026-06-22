from generated.array import Array
from generated.base_struct import BaseStruct


class SwitchParams(BaseStruct):
    e_group_type: int
    u_group_i_d: int
    u_default_switch: int
    num_switch_assoc: int
    ul_switch_assoc: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
