from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.path.structs.PathJoinPartResource import PathJoinPartResource


class PathJoinPartResourceRoot(MemStruct):
    resources_list: ArrayPointer[PathJoinPartResource]
    num_res: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
