from generated.formats.motiongraph.compounds.ActivityReference import ActivityReference
from generated.formats.motiongraph.compounds.Transition import Transition
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MRFMember2(MemStruct):
    transition: Pointer[Transition]
    count_0: int
    trigger: Pointer[str]
    activities: Pointer[ActivityReference]
    count_3_a: int
    count_3_b: int
    count_3_c: int
    num_activities: int
    count_5: int
    count_6_a: int
    count_6_b: int
    count_6_c: int
    id: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
