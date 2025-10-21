from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.scaleformlanguagedata.compounds.FontInfo import FontInfo


class ScaleformlanguagedataRoot(MemStruct):
    zero_0: int
    zero_1: int
    fonts: ArrayPointer[FontInfo]
    count: int
    zero_2: int
    zero_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
