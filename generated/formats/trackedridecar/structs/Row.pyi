from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackedridecar.structs.Seat import Seat


class Row(MemStruct):
    offset: float
    u_0: int
    seats: ArrayPointer[Seat]
    seats_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
