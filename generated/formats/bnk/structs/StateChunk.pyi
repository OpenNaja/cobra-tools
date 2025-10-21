from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.AkStateGroupChunk import AkStateGroupChunk
from generated.formats.bnk.structs.AkStatePropertyInfo import AkStatePropertyInfo


class StateChunk(BaseStruct):
    ul_num_state_props: int
    state_props: Array[AkStatePropertyInfo]
    ul_num_state_groups: int
    state_groups: Array[AkStateGroupChunk]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
