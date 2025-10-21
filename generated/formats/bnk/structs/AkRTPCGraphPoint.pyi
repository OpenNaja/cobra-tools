from generated.base_struct import BaseStruct


class AkRTPCGraphPoint(BaseStruct):
    from_v: float
    to_v: float
    interp: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
