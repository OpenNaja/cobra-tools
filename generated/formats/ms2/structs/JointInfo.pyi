from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.structs.HitCheck import HitCheck


class JointInfo(BaseStruct):
    eleven: int
    ff_1: int
    ff_2: int
    ff_3: int
    ff_4: int
    zero_0: int
    zero_1: int
    minus_1: int
    name: str
    hitcheck_count: int
    zero_2_a: int
    zero_2: int
    hitcheck_pointers: Array[int]
    hitchecks: Array[HitCheck]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
