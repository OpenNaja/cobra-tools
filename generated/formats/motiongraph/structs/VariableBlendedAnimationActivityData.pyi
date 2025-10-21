from generated.formats.motiongraph.structs.FloatInputData import FloatInputData
from generated.formats.motiongraph.structs.VariableBlendedAnimationData import VariableBlendedAnimationData
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class VariableBlendedAnimationActivityData(MemStruct):
    priorities: int
    _pad: int
    weight: FloatInputData
    animations: ArrayPointer[VariableBlendedAnimationData]
    animation_count: int
    variable: Pointer[str]
    variable_blended_animation_flags: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
