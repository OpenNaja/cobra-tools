from generated.base_struct import BaseStruct


class MaterialName(BaseStruct):
    name_index: int
    blend_mode: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
