from generated.formats.motiongraph.compounds.ActivityReference import ActivityReference
from generated.formats.motiongraph.compounds.MrfReference1 import MrfReference1
from generated.formats.motiongraph.compounds.MrfReference2 import MrfReference2
from generated.formats.motiongraph.compounds.XMLEntry import XMLEntry
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MotiongraphRootFrag(MemStruct):
    num_activities: int
    activities: ArrayPointer[ActivityReference]
    num_mrf_1: int
    mrf_1: ArrayPointer[MrfReference1]
    num_mrf_2: int
    mrf_2: ArrayPointer[MrfReference2]
    num_xmls: int
    xmls: ArrayPointer[XMLEntry]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
