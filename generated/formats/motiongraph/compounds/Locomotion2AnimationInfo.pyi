from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Locomotion2AnimationInfo(MemStruct):
    anim_name: Pointer[str]
    phase_entry_window: float
    priority: int
    anim_type: int
    _pad: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
