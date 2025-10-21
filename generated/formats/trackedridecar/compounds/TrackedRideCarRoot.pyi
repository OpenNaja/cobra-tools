from generated.array import Array
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.trackedridecar.compounds.Row import Row


class TrackedRideCarRoot(MemStruct):
    seat_rows: ArrayPointer[Row]
    seat_rows_count: int
    total_seats_count: int
    sizes: Array[float]
    zero_0: int
    hitcheck_model_name: Pointer[str]
    cabin_geometry_attach: Pointer[str]
    cabin_geometry: Pointer[str]
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
