from generated.formats.motiongraph.compounds.FloatInputData import FloatInputData
from generated.formats.motiongraph.compounds.VariableBlendedAnimationData import VariableBlendedAnimationData
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class VariableBlendedAnimationActivityData(MemStruct):
    priorities: int
    _pad: int
    weight: FloatInputData
    animations: ArrayPointer[VariableBlendedAnimationData]
    animation_count: int
    variable: Pointer[str]
    variable_blended_animation_flags: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
