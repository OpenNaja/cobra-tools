from generated.formats.habitatboundary.structs.HbOffsets import HbOffsets
from generated.formats.habitatboundary.structs.HbUiOptions import HbUiOptions
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class HabitatBoundaryDataRoot(MemStruct):
    prefab: Pointer[str]
    walls_extrusion: Pointer[str]
    walls_extrusion_end: Pointer[str]
    walls_extrusion_top: Pointer[str]
    walls_extrusion_cap_top: Pointer[str]
    walls_extrusion_bottom: Pointer[str]
    walls_unk_2: Pointer[str]
    walls_unk_3: Pointer[str]
    walls_unk_4: Pointer[str]
    walls_extrusion_door_cap_side: Pointer[str]
    walls_extrusion_door_cap_end: Pointer[str]
    walls_extrusion_door_cap_underside: Pointer[str]
    climb_proof_data: Pointer[str]
    broken_post: Pointer[str]
    broken_extrusion: Pointer[str]
    broken_extrusion_pile: Pointer[str]
    broken_ground: Pointer[str]
    broken_1_m: Pointer[str]
    broken_10_m: Pointer[str]
    post: Pointer[str]
    post_cap: Pointer[str]
    u_1: int
    u_2: float
    u_3: int
    ui_options: HbUiOptions
    u_4: float
    u_5: float
    offsets: HbOffsets
    wall_replace_level: int
    type: int
    padding: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
