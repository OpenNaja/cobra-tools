from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.researchdata.structs.ResearchFXData import ResearchFXData


class ResearchAffectedSquaddata(MemStruct):
    affected_squaddata_from: Pointer[object]
    affected_squaddata_to: Pointer[object]
    affected_squad_transition_fx: Pointer[ResearchFXData]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
