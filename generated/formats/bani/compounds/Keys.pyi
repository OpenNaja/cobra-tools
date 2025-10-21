import numpy as np
from generated.array import Array
from generated.formats.bani.compounds.Bone import Bone
from generated.formats.ovl_base.compounds.NestedPointers import NestedPointers


class Keys(NestedPointers):
    data: np.ndarray[tuple[int, int], np.dtype[Bone]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
