from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.techtree.compounds.ResearchDataDep import ResearchDataDep


class MutexResearch(MemStruct):
    mutex_options: ArrayPointer[ResearchDataDep]
    mutex_options_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
