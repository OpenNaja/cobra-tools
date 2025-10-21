from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ButtonData(MemStruct):
    k_1_a: int
    k_1_b: int
    k_2: int
    k_3: int
    k_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
