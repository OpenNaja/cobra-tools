from generated.base_struct import BaseStruct


class AkMediaInformation(BaseStruct):
    source_i_d: int
    u_in_memory_media_size: int
    u_source_bits: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
