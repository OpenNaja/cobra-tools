from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.researchdata.compounds.ResearchAffectedSquadloadout import ResearchAffectedSquadloadout


class ResearchAffectSquadloadouts(MemStruct):
    research_loc: ArrayPointer[ResearchAffectedSquadloadout]
    affected_squadloadout_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
