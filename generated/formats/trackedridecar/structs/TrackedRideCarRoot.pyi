from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.trackedridecar.structs.Row import Row


class TrackedRideCarRoot(MemStruct):
    seat_rows: ArrayPointer[Row]
    seat_rows_count: int
    total_seats_count: int
    sizes: Vector3
    sizes_align: int
    hitcheck_model_name: Pointer[str]
    cabin_geometry_attach: Pointer[str]
    cabin_geometry: Pointer[str]
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
