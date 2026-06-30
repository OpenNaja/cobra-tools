from generated.base_struct import BaseStruct


class SmallChunk(BaseStruct):
    a: int
    b: int
    c: int
    d: int
    flag: int
    e: int
    f: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
