from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.FadeParams import FadeParams


class TransParams(BaseStruct):
    src_fade_params: FadeParams
    e_sync_type: int
    u_cue_filter_hash: int
    dest_fade_params: FadeParams

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
