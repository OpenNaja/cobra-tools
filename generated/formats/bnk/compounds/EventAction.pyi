from generated.array import Array
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.compounds.NodeInitialParams import NodeInitialParams
from generated.formats.bnk.enums.ActionScope import ActionScope
from generated.formats.bnk.enums.ActionType import ActionType


class EventAction(HircObject):
    scope: ActionScope
    action_type: ActionType
    children: Array[int]
    id_ext_4: int
    node_initial_params: NodeInitialParams
    raw: Array[int]
    by_bit_vector: int
    bank_i_d: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
