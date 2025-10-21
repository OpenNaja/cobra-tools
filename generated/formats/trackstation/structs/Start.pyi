from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Start(MemStruct):
    element: Pointer[str]
    entrance: Pointer[str]
    rear: Pointer[str]
    middle: Pointer[str]
    front: Pointer[str]
    front_gate: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
