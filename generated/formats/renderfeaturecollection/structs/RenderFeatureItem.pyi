from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.renderfeaturecollection.structs.RenderFeatureSubItem import RenderFeatureSubItem


class RenderFeatureItem(MemStruct):
    item_name: Pointer[str]
    item_data: ArrayPointer[RenderFeatureSubItem]
    item_data_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
