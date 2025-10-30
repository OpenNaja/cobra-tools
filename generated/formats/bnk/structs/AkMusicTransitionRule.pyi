from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.AkMusicTransDstRule import AkMusicTransDstRule
from generated.formats.bnk.structs.AkMusicTransSrcRule import AkMusicTransSrcRule
from generated.formats.bnk.structs.AkMusicTransitionObject import AkMusicTransitionObject


class AkMusicTransitionRule(BaseStruct):
    u_num_src: int
    src_i_d: Array[int]
    u_num_dst: int
    dst_i_d: Array[int]
    src_rule: AkMusicTransSrcRule
    dst_rule: AkMusicTransDstRule
    alloc_trans_object_flag: int
    transition_object: AkMusicTransitionObject

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
