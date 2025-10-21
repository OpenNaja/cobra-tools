from typing import Union
from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.renderparameters.structs.ZStrPtr import ZStrPtr


class ParamData(MemStruct):
    data: Union[Array[ZStrPtr], Array[bool], Array[float], Array[int]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
