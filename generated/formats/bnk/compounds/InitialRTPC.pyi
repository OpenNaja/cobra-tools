from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.Rtpc import Rtpc


class InitialRTPC(BaseStruct):
    ul_num_r_t_p_c: int
    p_r_t_p_c_mgr: Array[Rtpc]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
