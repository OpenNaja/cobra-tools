from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class GuestAnimationInteractionList(MemStruct):
    type: int
    unk_0: int
    interact_in: Pointer[str]
    interact_loop: Pointer[str]
    interact_out: Pointer[str]
    interact_idle: Pointer[ZStringList]
    interact_idle_count: int
    unk_0: int
    interaction_grab: Pointer[str]
    interaction_good: Pointer[str]
    interaction_neutral: Pointer[str]
    interaction_bad: Pointer[str]
    interaction_none: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
