from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.techtree.compounds.MutexResearch import MutexResearch
from generated.formats.techtree.compounds.ResearchDataDep import ResearchDataDep


class TechLevel(MemStruct):
    automatic_research: ArrayPointer[ResearchDataDep]
    automatic_research_count: int
    unknown_0: int
    unlockable_research: ArrayPointer[ResearchDataDep]
    unlockable_research_count: int
    unknown_1: int
    mutexed_unlockable_research: ArrayPointer[MutexResearch]
    mutexed_unlockable_research_count: int
    unknown_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
