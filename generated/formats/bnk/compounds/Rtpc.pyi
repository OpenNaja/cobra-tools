from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.AkRTPCGraphPoint import AkRTPCGraphPoint


class Rtpc(BaseStruct):
    rtpcid: int
    rtpc_type: int
    rtpc_accum: int
    param_i_d: int
    rtpc_curve_i_d: int
    e_scaling: int
    ul_size: int
    graph: Array[AkRTPCGraphPoint]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
