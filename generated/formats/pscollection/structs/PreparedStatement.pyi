from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.pscollection.structs.Arg import Arg


class PreparedStatement(MemStruct):
    args: ArrayPointer[Arg]
    arg_count: int
    statement_name: Pointer[str]
    sql_query: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
