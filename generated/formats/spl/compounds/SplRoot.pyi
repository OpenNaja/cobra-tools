from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.spl.compounds.SplData import SplData


class SplRoot(MemStruct):
    spline_data: Pointer[SplData]
    count: int
    sixteen: int
    one: int
    length: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
