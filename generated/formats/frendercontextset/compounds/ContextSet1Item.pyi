from generated.formats.frendercontextset.compounds.ContextSet1SubItem import ContextSet1SubItem
from generated.formats.frendercontextset.compounds.LayerMap import LayerMap
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ContextSet1Item(MemStruct):
    stuff_1_name: Pointer[str]
    stuff_11_sub: ArrayPointer[ContextSet1SubItem]
    stuff_11_sub_count: int
    layer_maps: ArrayPointer[LayerMap]
    layer_maps_count: int
    stuff_13_sub: ArrayPointer[ContextSet1SubItem]
    stuff_13_sub_count: int
    stuff_14_sub_name: Pointer[str]
    stuff_15_sub_name: Pointer[str]
    stuff_16_sub_name: Pointer[str]
    stuff_1_unknown_1: int
    stuff_1_unknown_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
