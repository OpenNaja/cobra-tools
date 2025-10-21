from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.pscollection.structs.PreparedStatement import PreparedStatement


class PscollectionRoot(MemStruct):
    prepared_statements: ArrayPointer[PreparedStatement]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
