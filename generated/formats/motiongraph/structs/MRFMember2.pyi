from generated.formats.motiongraph.structs.ActivityReference import ActivityReference
from generated.formats.motiongraph.structs.CurveData import CurveData
from generated.formats.motiongraph.structs.Transition import Transition
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MRFMember2(MemStruct):
    transition: Pointer[Transition]
    curve: Pointer[CurveData]
    trigger: Pointer[str]
    activities: Pointer[ActivityReference]
    float_0: float
    count_3_c: int
    num_activities: int
    other_mrf: Pointer[MRFMember2]
    count_6_a: int
    count_6_b: int
    count_6_c: int
    id: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
