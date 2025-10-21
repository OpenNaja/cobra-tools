from generated.array import Array
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class UiMovieHeader(MemStruct):
    movie_name: Pointer[str]
    pkg_name: Pointer[str]
    category_name: Pointer[str]
    type_name: Pointer[str]
    flag_1: int
    flag_2: int
    flag_3: int
    floats: Array[float]
    u_0: int
    num_ui_triggers: int
    u_1: int
    num_ui_names: int
    num_assetpkgs: int
    u_2: int
    num_list_1: int
    num_list_2: int
    num_ui_interfaces: int
    u_3: int
    u_4: int
    u_5: int
    ptr_0: Pointer[object]
    ui_triggers: Pointer[ZStringList]
    ptr_1: Pointer[object]
    ui_names: Pointer[ZStringList]
    assetpkgs: Pointer[ZStringList]
    ptr_2: Pointer[object]
    list_1: ArrayPointer[int]
    list_2: ArrayPointer[int]
    ui_interfaces: Pointer[ZStringList]
    ptr_3: Pointer[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
