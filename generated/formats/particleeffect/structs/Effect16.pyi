from generated.array import Array
from generated.formats.particleeffect.structs.Effect import Effect


class Effect16(Effect):
    ints: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
