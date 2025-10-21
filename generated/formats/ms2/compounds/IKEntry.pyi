from generated.base_struct import BaseStruct
from generated.formats.ms2.compounds.BonePointer import BonePointer
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.RotationRange import RotationRange


class IKEntry(BaseStruct):
    child: BonePointer
    parent: BonePointer
    unk_0: int
    matrix: Matrix33
    yaw: RotationRange
    pitch: RotationRange
    unk_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
