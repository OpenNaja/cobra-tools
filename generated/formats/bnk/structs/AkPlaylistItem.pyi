from generated.base_struct import BaseStruct


class AkPlaylistItem(BaseStruct):
    ul_play_i_d: int
    weight: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
