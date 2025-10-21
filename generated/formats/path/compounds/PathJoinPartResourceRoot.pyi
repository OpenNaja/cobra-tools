from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.compounds.PathJoinPartResource import PathJoinPartResource


class PathJoinPartResourceRoot(MemStruct):
    resources_list: ArrayPointer[PathJoinPartResource]
    num_res: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
