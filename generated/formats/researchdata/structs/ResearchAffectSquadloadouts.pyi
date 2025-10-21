from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.researchdata.structs.ResearchAffectedSquadloadout import ResearchAffectedSquadloadout


class ResearchAffectSquadloadouts(MemStruct):
    research_loc: ArrayPointer[ResearchAffectedSquadloadout]
    affected_squadloadout_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
