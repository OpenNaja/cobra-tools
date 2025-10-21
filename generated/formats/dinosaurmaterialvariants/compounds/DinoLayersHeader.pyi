from generated.formats.dinosaurmaterialvariants.compounds.CommonHeader import CommonHeader
from generated.formats.dinosaurmaterialvariants.compounds.Layer import Layer
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer


class DinoLayersHeader(CommonHeader):
    layers: ArrayPointer[Layer]
    layer_count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
