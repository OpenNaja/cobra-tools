from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.renderfeaturecollection.compounds.RenderFeatureSubItem import RenderFeatureSubItem


class RenderFeatureItem(MemStruct):
    item_name: Pointer[str]
    item_data: ArrayPointer[RenderFeatureSubItem]
    item_data_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
