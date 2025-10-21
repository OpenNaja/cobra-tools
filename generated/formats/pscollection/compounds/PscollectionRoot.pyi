from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.pscollection.compounds.PreparedStatement import PreparedStatement


class PscollectionRoot(MemStruct):
    prepared_statements: ArrayPointer[PreparedStatement]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
