from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class GenericInfo(MemStruct):
    _name_offset: int
    dtype: FgmDtype

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
