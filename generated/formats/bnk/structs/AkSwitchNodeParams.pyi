from generated.base_struct import BaseStruct


class AkSwitchNodeParams(BaseStruct):
    ul_node_i_d: int
    by_bit_vector_1: int
    by_bit_vector_2: int
    fade_out_time: int
    fade_in_time: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
