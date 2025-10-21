from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ClimbproofDataRoot(MemStruct):
    climb_proof: Pointer[str]
    climb_proof_cap_start: Pointer[str]
    climb_proof_cap_end: Pointer[str]
    climb_proof_bracket: Pointer[str]
    post_gap: float
    u_1: float
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
