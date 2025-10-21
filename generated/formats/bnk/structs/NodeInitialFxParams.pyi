from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.FXChunk import FXChunk


class NodeInitialFxParams(BaseStruct):
    b_is_override_parent_f_x: int
    u_num_fx: int
    bits_f_x_bypass: int
    fx: Array[FXChunk]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
