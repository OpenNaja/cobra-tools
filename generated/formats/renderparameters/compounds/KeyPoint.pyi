from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.renderparameters.compounds.ParamData import ParamData


class KeyPoint(MemStruct):
    time: float
    value: ParamData
    tangent_before: float
    tangent_after: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
