from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.researchdata.structs.AppliedGlobalBuff import AppliedGlobalBuff
from generated.formats.researchdata.structs.ResearchAffectSquadloadouts import ResearchAffectSquadloadouts
from generated.formats.researchdata.structs.ResearchAffectedSquaddata import ResearchAffectedSquaddata
from generated.formats.researchdata.structs.ResearchDataAppliesToSquad import ResearchDataAppliesToSquad
from generated.formats.researchdata.structs.ResearchDescriptionLoc import ResearchDescriptionLoc
from generated.formats.researchdata.structs.SquadReplacementData import SquadReplacementData


class ResearchRoot(MemStruct):
    ptr_0: Pointer[str]
    int_0: int
    int_1: int
    research_name: Pointer[str]
    research_icon: Pointer[str]
    research_icon_queued: Pointer[str]
    unk_1: int
    research_cost_realmstone: int
    int_2: int
    research_duration: int
    unk_3: int
    applied_global_buff: Pointer[AppliedGlobalBuff]
    research_replace_squad_variants: ArrayPointer[ResearchAffectedSquaddata]
    research_replace_squad_variants_count: int
    affected_squad_loc: Pointer[str]
    unit_path: Pointer[str]
    research_description: ArrayPointer[ResearchDescriptionLoc]
    research_description_count: int
    research_flavor_text: Pointer[str]
    applies_to_squad: ArrayPointer[ResearchDataAppliesToSquad]
    applies_to_squad_count: int
    research_affected_squadloadouts: Pointer[ResearchAffectSquadloadouts]
    unk_9: int
    research_replaceds_squads: Pointer[SquadReplacementData]
    replacement_squad_data_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
