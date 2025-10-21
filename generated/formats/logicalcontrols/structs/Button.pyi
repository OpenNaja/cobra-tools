from generated.formats.logicalcontrols.structs.ButtonData import ButtonData
from generated.formats.logicalcontrols.structs.PCButtonData import PCButtonData
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Button(MemStruct):
    button_name: Pointer[str]
    datas: ArrayPointer[ButtonData]
    pcdatas: ArrayPointer[PCButtonData]
    datas_count: int
    flags: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
