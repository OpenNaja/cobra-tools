from generated.formats.frenderfeatureset.compounds.FeatureSetItem import FeatureSetItem
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FRenderFeatureSetRoot(MemStruct):
    featureset_list: ArrayPointer[FeatureSetItem]
    featureset_count: int
    unknown_always_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
