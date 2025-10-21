from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ppuipkg.compounds.Ppuipkgfile import Ppuipkgfile
from generated.formats.ppuipkg.compounds.UserInterfaceIconData import UserInterfaceIconData


class PPUIPKGRoot(MemStruct):
    basic_path: Pointer[str]
    file_count: int
    files: ArrayPointer[Ppuipkgfile]
    icondata_count: int
    types: ArrayPointer[UserInterfaceIconData]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
