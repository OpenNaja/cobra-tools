from generated.base_struct import BaseStruct


class AkMusicMarkerWwise(BaseStruct):
    id: int
    f_position: float
    u_string_size: int
    p_marker_name: str

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
