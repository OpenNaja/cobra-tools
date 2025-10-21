from generated.formats.navigationsettings.compounds.NavigationAreaCostsFilter import NavigationAreaCostsFilter
from generated.formats.navigationsettings.compounds.NavigationModeFilter import NavigationModeFilter
from generated.formats.navigationsettings.compounds.NavigationTestList import NavigationTestList
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class NavigationSettingsRoot(MemStruct):
    settings_count: int
    settings_default_name: Pointer[str]
    navigation_source_types: Pointer[ZStringList]
    navigation_source_types_count: int
    navigation_flags: Pointer[ZStringList]
    navigation_flags_count: int
    navigation_test: ArrayPointer[NavigationTestList]
    navigation_test_count: int
    navigation_area_costs_filter_names: ArrayPointer[NavigationAreaCostsFilter]
    navigation_area_costs_filter_names_count: int
    navigation_mode_filter_names: ArrayPointer[NavigationModeFilter]
    navigation_mode_filter_names_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
