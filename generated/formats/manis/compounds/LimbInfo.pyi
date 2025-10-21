from generated.base_struct import BaseStruct


class LimbInfo(BaseStruct):
    zeros_0: int
    bone: int
    counta: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
