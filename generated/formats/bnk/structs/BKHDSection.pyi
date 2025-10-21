from generated.array import Array
from generated.base_struct import BaseStruct


class BKHDSection(BaseStruct):
    length: int
    version: int
    dw_sound_bank_i_d: int
    dw_language_i_d: int
    u_alignment: int
    b_device_allocated: int
    dw_project_i_d: int
    padding: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
