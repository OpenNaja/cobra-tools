from generated.formats.motiongraph.structs.ActivityReference import ActivityReference
from generated.formats.motiongraph.structs.MrfReference1 import MrfReference1
from generated.formats.motiongraph.structs.MrfReference2 import MrfReference2
from generated.formats.motiongraph.structs.XMLEntry import XMLEntry
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


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
