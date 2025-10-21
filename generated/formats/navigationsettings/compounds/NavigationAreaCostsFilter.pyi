from generated.formats.navigationsettings.compounds.NavigationAreaCostsData import NavigationAreaCostsData
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class NavigationAreaCostsFilter(MemStruct):
    navigation_area_costs_filter_name: Pointer[str]
    navigation_area_costs: ArrayPointer[NavigationAreaCostsData]
    navigation_area_costs_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
