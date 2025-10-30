from generated.base_struct import BaseStruct


class FadeParams(BaseStruct):
    transition_time: int
    e_fade_curve: int
    i_fade_offset: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
