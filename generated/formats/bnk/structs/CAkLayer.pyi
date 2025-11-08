from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.CAssociatedChildData import CAssociatedChildData
from generated.formats.bnk.structs.InitialRTPC import InitialRTPC


class CAkLayer(BaseStruct):
    ul_layer_i_d: int
    initial_r_t_p_c: InitialRTPC
    rtpc_i_d: int
    rtpc_type: int
    ul_num_assoc: int
    assocs: Array[CAssociatedChildData]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
