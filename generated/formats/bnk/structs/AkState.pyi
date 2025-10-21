from generated.base_struct import BaseStruct


class AkState(BaseStruct):
    ul_state_i_d: int
    ul_state_instance_i_d: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
