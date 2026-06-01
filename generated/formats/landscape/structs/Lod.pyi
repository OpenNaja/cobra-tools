from generated.base_struct import BaseStruct


class Lod(BaseStruct):
    index: int
    unk: int
    unk_2: int
    index_1: int
    distance: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
