from generated.array import Array
from generated.formats.base.compounds.ZStringBuffer import ZStringBuffer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PhysmatRoot(MemStruct):
    all_surfaces_count: int
    surface_res_count: int
    classnames_count: int
    stringbuffer_size: int
    pointers: Array[int]
    all_surfaces_flags: Array[int]
    surface_res_indices: Array[int]
    all_surfaces_names: Array[int]
    surface_res_names: Array[int]
    classnames_names: Array[int]
    classnames_indices: Array[int]
    names: ZStringBuffer

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
