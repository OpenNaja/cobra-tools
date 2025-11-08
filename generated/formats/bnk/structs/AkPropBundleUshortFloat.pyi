from generated.base_struct import BaseStruct


class AkPropBundleUshortFloat(BaseStruct):
    p_i_d: int
    p_value: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
