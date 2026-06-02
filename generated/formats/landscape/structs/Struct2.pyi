from generated.array import Array
from generated.base_struct import BaseStruct


class Struct2(BaseStruct):
    a: int
    b: int
    z: int
    c: int
    d: int
    floats: Array[Array[float]]
    e: Array[int]
    floats_2: Array[float]
    f: Array[int]
    floats_3: Array[float]
    g: int
    h: int
    i: int
    j: int
    zfinal: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
