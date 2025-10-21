from generated.base_struct import BaseStruct


class Vector3Ushort(BaseStruct):
    x: int
    y: int
    z: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
