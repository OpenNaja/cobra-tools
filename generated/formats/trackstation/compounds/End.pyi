from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class End(MemStruct):
    element: Pointer[str]
    start: Pointer[str]
    middle: Pointer[str]
    end: Pointer[str]
    support: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
