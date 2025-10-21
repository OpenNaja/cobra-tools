from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.renderfeaturecollection.structs.RenderFeatureItem import RenderFeatureItem


class RenderFeatureCollectionRoot(MemStruct):
    item_list: ArrayPointer[RenderFeatureItem]
    item_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
