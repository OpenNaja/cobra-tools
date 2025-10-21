from generated.formats.dinosaurmaterialvariants.structs.CommonHeader import CommonHeader
from generated.formats.dinosaurmaterialvariants.structs.Layer import Layer
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer


class DinoLayersHeader(CommonHeader):
    layers: ArrayPointer[Layer]
    layer_count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
