from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackedridecar.compounds.Seat import Seat


class Row(MemStruct):
    offset: float
    u_0: int
    seats: ArrayPointer[Seat]
    seats_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
