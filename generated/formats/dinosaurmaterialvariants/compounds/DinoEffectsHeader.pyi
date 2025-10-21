from generated.array import Array
from generated.formats.dinosaurmaterialvariants.compounds.CommonHeader import CommonHeader
from generated.formats.dinosaurmaterialvariants.compounds.Vector3F import Vector3F


class DinoEffectsHeader(CommonHeader):
    vec_0: Vector3F
    vec_1: Vector3F
    a: int
    b: int
    vec_2: Vector3F
    vec_3: Vector3F
    vec_4: Vector3F
    vec_5: Vector3F
    c: int
    d: int
    floats_1: Array[float]
    e: int
    floats_2: Array[float]
    f: int
    floats_3: Array[float]
    g: int
    floats_4: Array[float]
    h: int
    floats_5: Array[float]
    i: int
    float: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
