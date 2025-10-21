from generated.formats.dlcentitlements.structs.Entitlement import Entitlement
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DLCEntitlementsRoot(MemStruct):
    entitlement_list: ArrayPointer[Entitlement]
    entitlement_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
