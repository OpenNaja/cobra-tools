from generated.formats.motiongraph.compounds.MRFMember2 import MRFMember2
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MrfReference2(MemStruct):
    value: Pointer[MRFMember2]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
