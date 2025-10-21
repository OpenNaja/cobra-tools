from generated.base_struct import BaseStruct


class Segment(BaseStruct):
    unk_a: int
    unk_b: int
    ptr_ori_result: int
    ptr_pos_result: int
    ptr_scale_0_result: int
    ptr_scale_1_result: int
    ptr_morph_result: int
    ptr_compressed_mani_data: int
    byte_size: int
    ptr_compressed_keys: int
    zeros_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
