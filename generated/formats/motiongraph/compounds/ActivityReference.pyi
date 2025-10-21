from generated.formats.motiongraph.compounds.Activity import Activity
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ActivityReference(MemStruct):
    activity: Pointer[Activity]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
