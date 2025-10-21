from generated.base_struct import BaseStruct


class AdvSettingsParams(BaseStruct):
    by_bit_vector: int
    e_virtual_queue_behavior: int
    u_16_max_num_instance: int
    e_below_threshold_behavior: int
    by_bit_vector: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
