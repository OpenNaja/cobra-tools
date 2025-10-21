from generated.formats.motiongraph.structs.MRFMember1 import MRFMember1
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MrfReference1(MemStruct):
    value: Pointer[MRFMember1]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
