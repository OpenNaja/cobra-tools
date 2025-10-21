from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class NavigationAreaCostsData(MemStruct):
    navigation_area_name: Pointer[str]
    navigation_area_weight_1: float
    navigation_area_weight_2: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
