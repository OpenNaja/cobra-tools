from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.AkRTPCGraphPoint import AkRTPCGraphPoint


class AkClipAutomation(BaseStruct):
    u_clip_index: int
    e_auto_type: int
    u_num_points: int
    graph: Array[AkRTPCGraphPoint]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
