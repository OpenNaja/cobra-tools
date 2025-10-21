from generated.array import Array
from generated.formats.particleeffect.structs.Effect import Effect


class Effect08(Effect):
    floats: Array[float]
    minus_1: int
    angle: Array[float]
    floats_2: Array[float]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
