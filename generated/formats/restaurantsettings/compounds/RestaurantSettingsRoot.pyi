from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.restaurantsettings.compounds.Perk import Perk


class RestaurantSettingsRoot(MemStruct):
    running_cost_base: int
    unk_1: int
    unk_2: float
    unk_3: float
    unk_4: float
    unk_5: float
    unk_6: float
    running_cost_per_extension: int
    unk_8: int
    unk_9: float
    perks: ArrayPointer[Perk]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
