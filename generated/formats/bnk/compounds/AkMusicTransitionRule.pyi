from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.AkMusicTransDstRule import AkMusicTransDstRule
from generated.formats.bnk.compounds.AkMusicTransSrcRule import AkMusicTransSrcRule


class AkMusicTransitionRule(BaseStruct):
    u_num_src: int
    src_i_d: Array[int]
    u_num_dst: int
    dst_i_d: Array[int]
    src_rule: AkMusicTransSrcRule
    dst_rule: AkMusicTransDstRule
    alloc_trans_object_flag: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
