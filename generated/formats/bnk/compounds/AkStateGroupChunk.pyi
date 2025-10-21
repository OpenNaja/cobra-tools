from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.AkState import AkState


class AkStateGroupChunk(BaseStruct):
    ul_state_group_i_d: int
    e_state_sync_type: int
    ul_num_states: int
    states: Array[AkState]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
