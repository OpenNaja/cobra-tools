from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Perk(MemStruct):
    unk_0: int
    building_cost: int
    running_cost_base: int
    running_cost_per_extension: int
    unk_4: float
    unk_5: float
    label: Pointer[str]
    desc: Pointer[str]
    icon: Pointer[str]
    unk_6: float
    appeal_adults: float
    appeal_families: float
    appeal_teenagers: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
