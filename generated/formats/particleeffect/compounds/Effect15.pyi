from generated.array import Array
from generated.formats.particleeffect.compounds.Effect import Effect


class Effect15(Effect):
    floats_1: Array[float]
    flags: Array[int]
    floats_2: Array[float]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
