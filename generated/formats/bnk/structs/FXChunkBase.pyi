from generated.base_struct import BaseStruct


class FXChunkBase(BaseStruct):
    u_f_x_index: int
    fx_i_d: int
    b_is_share_set: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
