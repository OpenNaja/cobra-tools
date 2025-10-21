from generated.formats.matcol.compounds.RootFrag import RootFrag
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MatcolRoot(MemStruct):
    main: Pointer[RootFrag]
    one: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
