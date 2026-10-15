from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ppuipkg.structs.Base64ArrayPointer import Base64ArrayPointer


class Ppuipkgfile(MemStruct):
    file_name: Pointer[str]
    file_size: int
    file_content: Base64ArrayPointer[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
