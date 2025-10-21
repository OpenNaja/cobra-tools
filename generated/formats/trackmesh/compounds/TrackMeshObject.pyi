from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackMeshObject(MemStruct):
    place_id: Pointer[str]
    file: Pointer[str]
    type: int
    b: int
    c: int
    xtra_1: float
    xtra_2: int
    attachment_start: Pointer[str]
    attachment_end: Pointer[str]
    e: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
