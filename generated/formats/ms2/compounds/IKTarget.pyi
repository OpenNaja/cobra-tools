from generated.base_struct import BaseStruct
from generated.formats.ms2.compounds.BonePointer import BonePointer


class IKTarget(BaseStruct):
    ik_blend: BonePointer
    ik_end: BonePointer

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
