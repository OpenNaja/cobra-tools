from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.researchdata.structs.SubResearchFXData import SubResearchFXData


class ResearchFXData(MemStruct):
    unk_0: int
    research_complete_fx: Pointer[SubResearchFXData]
    unk_1: int
    unk_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
