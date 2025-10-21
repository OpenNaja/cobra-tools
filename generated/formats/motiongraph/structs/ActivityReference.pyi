from generated.formats.motiongraph.structs.Activity import Activity
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ActivityReference(MemStruct):
    activity: Pointer[Activity]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
